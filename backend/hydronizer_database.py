import logging
from datetime import datetime
import time
import random
conn = __import__('settings').global_conn

def create_table_if_not_exist():
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS water_breaks (id SERIAL PRIMARY KEY, deviceID STRING, date DATE, time TIME, quantity INT)")
    conn.commit()

def create_entry(message_id, time_sent, weight):
    with conn.cursor() as cur:
        create_table_if_not_exist()
        quantity = get_quantity(message_id)
        command = "INSERT INTO water_breaks (deviceID, date, time, quantity) VALUES (%s, %s, %s, %s)"
        formatted_date = datetime.now().strftime('%Y-%m-%d')
        formatted_time = datetime.now().strftime('%H:%M:%S')
        cur.execute(command, (message_id, formatted_date, formatted_time, quantity))
        logging.debug("create_entry(): status message: %s", cur.statusmessage)
    conn.commit()

def delete_entries():
    with conn.cursor() as cur:
        cur.execute("DELETE FROM hydronizer.water_breaks")
        logging.debug("delete_entries(): status message: %s", cur.statusmessage)
    conn.commit()

def print_breaks():
    with conn.cursor() as cur:
        cur.execute("SELECT id, time, quantity FROM water_breaks")
        logging.debug("print_breaks(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        print(f"Breaks at {time.asctime()}:")
        for row in rows:
            print(row)

def get_quantity(device):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM water_breaks WHERE deviceid = '" + device + "' ORDER BY id DESC LIMIT 1;"
        )
        rows = cur.fetchall()
        lastQuantity = int(rows[0][4])
        return lastQuantity - random.randrange(30,51)
    conn.commit()

def get_last_entry():
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM water_breaks ORDER BY ID DESC LIMIT 1"
        )
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
    conn.commit()
    return last_entry