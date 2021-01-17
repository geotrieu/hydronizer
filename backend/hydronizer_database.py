import logging
from datetime import datetime
import time
import random
conn = __import__('settings').global_conn

def create_table_if_not_exist():
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS water_breaks (id SERIAL PRIMARY KEY, deviceID TEXT, date DATE, time TIME, quantity INT, drank INT)")
    conn.commit()

def create_user_table_if_not_exist():
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS users (deviceID TEXT PRIMARY KEY, deviceName TEXT, timer INT)")
    conn.commit()

def update_time(device_id, device_name, new_time):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM users WHERE deviceID = '" + device_id + "';"
        )
        row = cur.fetchall()          
    conn.commit()

    if len(row) == 0:
        create_user(device_id, device_name, new_time)
    else:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET timer = " + str(new_time) + " WHERE deviceID = '" + device_id + "';"
            )
        conn.commit()
    
    return {"device_id": device_name, "device_name": device_name, "timer": new_time}

def create_user(device_id, device_name, new_time):
    create_user_table_if_not_exist()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO users (deviceID, deviceName, timer) VALUES ('" + device_id + "', '" + device_name + "', " + str(new_time) + ");"
        )      
    conn.commit()

def get_user_name(device_id):
    create_user_table_if_not_exist()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM users WHERE deviceid = '" + device_id + "';"
        )
        rows = cur.fetchall()

        if len(rows) == 0:
            print(rows)
            create_user(device_id, device_id, 1800)
            return str(device_id)

        return str(rows[0][1])
    conn.commit()

def get_user_time(device_id):
    create_user_table_if_not_exist()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM users WHERE deviceID = '" + device_id + "';"
        )
        rows = cur.fetchall()

        if len(rows) == 0:
            print(rows)
            create_user(device_id, device_id, 1800)
            return {"device_id": device_id, "device_name": device_id,"timer": 1800}

        return {"device_id": device_id, "device_name": rows[0][1],"timer": rows[0][2]}
    conn.commit()

def create_entry(message_id, time_sent, weight):
    create_table_if_not_exist()
    with conn.cursor() as cur:
        quantities = get_quantities(message_id)
        command = "INSERT INTO water_breaks (deviceID, date, time, quantity, drank) VALUES (%s, %s, %s, %s, %s)"
        formatted_date = datetime.now().strftime('%Y-%m-%d')
        formatted_time = datetime.now().strftime('%H:%M:%S')
        cur.execute(command, (message_id, formatted_date, formatted_time, quantities[0], quantities[1]))
        logging.debug("create_entry(): status message: %s", cur.statusmessage)
    conn.commit()

def get_quantities(device):
    create_table_if_not_exist()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM water_breaks WHERE deviceid = '" + device + "' ORDER BY id DESC LIMIT 1;"
        )
        rows = cur.fetchall()
        if (len(rows) == 0): # New Water Bottle
            return [1500, 0]
        lastQuantity = int(rows[0][4])
        drank = random.randrange(30,51)
        return [lastQuantity - drank, drank]
    conn.commit()

def get_last_entry(device_id):
    create_table_if_not_exist()
    with conn.cursor() as cur:
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
    conn.commit()
    return last_entry

def get_metrics_db(device_id):
    create_table_if_not_exist()
    # returns number of sips from today, total water consumed, average, amount of water you need to 
    with conn.cursor() as cur:
        formatted_date = datetime.now().strftime('%Y-%m-%d')
        command = "SELECT * FROM water_breaks WHERE deviceid = '{}' AND date = '{}' ORDER BY time ASC;".format(device_id, formatted_date)
        cur.execute(command)
        data_today = cur.fetchall()
        print(data_today)
        print(type(data_today))
        num = len(data_today)
        print(num)
    conn.commit()

    total_today = 0
    for row in data_today:
        total_today += row[5]

    DAILY_RECOMMENDED = 2000
    amount_left = DAILY_RECOMMENDED - total_today
    if amount_left < 0:
        amount_left = 0
    
    with conn.cursor() as cur:
        command = "SELECT * FROM water_breaks WHERE deviceid = '{}';".format(device_id)
        cur.execute(command)
        all_data = cur.fetchall()
        total_consumed = 0
        for row in all_data:
            total_consumed += row[5]
    conn.commit()

    metrics = {
        "number_of_sips": num,
        "total_consumed_today": total_today,
        "total_consumed": total_consumed,
        "amount_left": amount_left
    }

    return metrics