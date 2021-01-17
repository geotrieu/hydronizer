import paho.mqtt.client as mqtt #import the client1
import time
import random
import logging
import json
import random
from datetime import datetime
from argparse import ArgumentParser, RawTextHelpFormatter

from flask import Flask, request, json
from flask_cors import CORS, cross_origin

import psycopg2
from psycopg2.errors import SerializationFailure

import threading

api = Flask(__name__)
CORS(api)
global_conn = None

#######################################
# MQTT client calls this whenever they receive a message from the broker
def on_message(client, userdata, message):
    data = json.loads(message.payload.decode("utf-8"))
    message_id = data['id']
    now = datetime.now()
    curr_time = now.strftime("%H:%M:%S")
    weight = data['weight']

    create_entry(message_id, curr_time, weight)
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)
########################################

########################################
# GET API for last water break
@api.route('/lastwaterbreak', methods=['GET'])

def get_last_water_break():
    device_id = request.args['arg1']
    return getLastEntry(device_id)
########################################


########################################
# GET API for metrics
@api.route('/metrics', methods=['GET'])
def get_metrics():
    device_id = request.args['arg1']
    return getMetrics(device_id)


def create_entry(message_id, time_sent, weight):
    with global_conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS water_breaks (id SERIAL PRIMARY KEY, deviceID STRING, date DATE, time TIME, quantity INT)"
        )
        quantity = getQuantity(message_id)
        command = "INSERT INTO water_breaks (deviceID, date, time, quantity) VALUES (%s, %s, %s, %s)"
        formatted_date = datetime.now().strftime('%Y-%m-%d')
        formatted_time = datetime.now().strftime('%H:%M:%S')
        cur.execute(command, (message_id, formatted_date, formatted_time, quantity))
        logging.debug("create_entry(): status message: %s", cur.statusmessage)
    global_conn.commit()

def delete_entries(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM hydronizer.water_breaks")
        logging.debug("delete_entries(): status message: %s", cur.statusmessage)
    conn.commit()

def print_breaks(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, time, quantity FROM water_breaks")
        logging.debug("print_breaks(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        print(f"Breaks at {time.asctime()}:")
        for row in rows:
            print(row)

def test_retry_loop(conn):
    """
    Cause a seralization error in the connection.

    This function can be used to test retry logic.
    """
    with conn.cursor() as cur:
        # The first statement in a transaction can be retried transparently on
        # the server, so we need to add a dummy statement so that our
        # force_retry() statement isn't the first one.
        cur.execute("SELECT now()")
        cur.execute("SELECT crdb_internal.force_retry('1s'::INTERVAL)")
    logging.debug("test_retry_loop(): status message: %s", cur.statusmessage)

def getQuantity(device):
    with global_conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM water_breaks WHERE deviceid = '" + device + "' ORDER BY id DESC LIMIT 1;"
        )
        rows = cur.fetchall()
        lastQuantity = int(rows[0][4])
        return lastQuantity - random.randrange(30,51)
    global_conn.commit()

def getLastEntry(device_id):
    with global_conn.cursor() as cur:
        command = "SELECT * FROM water_breaks WHERE deviceid = '{}' ORDER BY id DESC LIMIT 1;".format(device_id)
        print(type(command))
        print(command)
        cur.execute(command)
        row = cur.fetchall()[0]

        last_entry = {
            "message_id": row[0],
            "device_id": row[1],
            "date": row[2].strftime("%Y-%m-%d"),
            "time": row[3].strftime("%H:%M:%S"),
            "quantity": row[4]
        }

        print(last_entry)
        print(type(last_entry))
    global_conn.commit()
    return last_entry

def getMetrics(device_id):
    # returns number of sips from today, total water consumed, average, amount of water you need to 
    with global_conn.cursor() as cur:
        formatted_date = datetime.now().strftime('%Y-%m-%d')
        command = "select * from water_breaks where deviceid = '{}' AND date = '{}' order by time ASC;".format(device_id, formatted_date)
        cur.execute(command)
        data_today = cur.fetchall()
        print(data_today)
        print(type(data_today))
        num = len(data_today)
        print(num)
    global_conn.commit()

    total_today = 0
    for row in data_today:
        total_today += row[4]
    

    DAILY_RECOMMENDED = 2000
    amount_left = DAILY_RECOMMENDED - total_today
    if amount_left < 0:
        amount_left = 0
    
    with global_conn.cursor() as cur:
        command = "select * from water_breaks where deviceid = '{}';".format(device_id)
        cur.execute(command)
        all_data = cur.fetchall()
        total_consumed = 0
        for row in all_data:
            total_consumed += row[4]
    global_conn.commit()

    metrics = {
        "number_of_sips": num,
        "total_consumed_today": total_today,
        "total_consumed": total_consumed,
        "amount_left": amount_left
    }

    return metrics
    
def main():
    opt = parse_cmdline()
    logging.basicConfig(level=logging.DEBUG if opt.verbose else logging.INFO)
    logging.getLogger('flask_cors').level = logging.DEBUG
    conn = psycopg2.connect(opt.dsn)
    global global_conn
    global_conn = conn

    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS water_breaks (id SERIAL PRIMARY KEY, deviceID STRING, date DATE, time TIME, quantity INT)"
        )
    conn.commit()

    broker_address="35.185.60.243"
    print("creating new instance")
    client = mqtt.Client() #create new instance
    client.on_message=on_message #attach function to callback
    print("connecting to broker")
    client.connect(broker_address) #connect to broker
    print("Subscribing to topic","hydronizer/reports")
    client.subscribe("hydronizer/reports")
    client.loop_forever()
    #print("Publishing message to topic","hydronizer/reports")
    #client.publish("hydronizer/reports",'{"id":"5843862085612977","weight":500}')
    time.sleep(30) # wait
    #client.loop_stop() #stop the loop
    #delete_entries(conn)

    # Close communication with the database.
    #conn.close()


def parse_cmdline():
    parser = ArgumentParser(description=__doc__,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "dsn",
        help="database connection string\n\n"
             "For cockroach demo, use postgresql://<username>:<password>@<hostname>:<port>/bank?sslmode=require,\n"
             "with the username and password created in the demo cluster, and the hostname and port listed in the\n"
             "(sql/tcp) connection parameters of the demo cluster welcome message."
    )

    parser.add_argument("-v", "--verbose",
                        action="store_true", help="print debug info")

    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    thread1 = threading.Thread(target = main, args = ())
    thread2 = threading.Thread(target = api.run, args = ())

    thread1.start()
    thread2.start()
    