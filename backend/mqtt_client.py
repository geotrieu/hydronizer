import paho.mqtt.client as mqtt #import the client1
import time
import random
import logging
import json
import random
from datetime import datetime
from argparse import ArgumentParser, RawTextHelpFormatter

import psycopg2
from psycopg2.errors import SerializationFailure

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

def create_entry(message_id, time_sent, weight):

    type(global_conn)
    with global_conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS water_breaks (id SERIAL PRIMARY KEY, deviceID STRING, date DATE, time TIME, quantity INT)"
        )
        quantity = getQuantity()
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

def getQuantity():
    type(global_conn)
    with global_conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM water_breaks WHERE deviceid = '54kilrgk5x909u4n' ORDER BY id DESC LIMIT 1;"
        )
        rows = cur.fetchall()
        lastQuantity = int(rows[0][4])
        return lastQuantity - random.randrange(30,51)
    global_conn.commit()


def main():
    opt = parse_cmdline()
    logging.basicConfig(level=logging.DEBUG if opt.verbose else logging.INFO)
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
    #time.sleep(20) # wait
    #client.loop_stop() #stop the loop

    #print_breaks(conn)

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
    main()
    