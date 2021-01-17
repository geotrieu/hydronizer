from datetime import datetime
import json
import paho.mqtt.client as mqtt

import settings
import hydronizer_database as db

def on_message(client, userdata, message):
    data = json.loads(message.payload.decode("utf-8"))
    message_id = data['id']
    now = datetime.now()
    curr_time = now.strftime("%H:%M:%S")
    weight = data['weight']

    username = db.get_user_name(message_id)
    settings.mqtt.publish("hydronizer/user", username)

    db.create_entry(message_id, curr_time, weight)
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)

broker_address="35.185.60.243" 
#broker_address="iot.eclipse.org" #use external broker
settings.mqtt = mqtt.Client() #create new instance
settings.mqtt.connect(broker_address) #connect to 
print("Connected to MQTT!")
settings.mqtt.on_message = on_message
settings.mqtt.subscribe("hydronizer/reports")
settings.mqtt.loop_start()