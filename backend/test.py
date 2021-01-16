import paho.mqtt.client as mqtt #import the client1
import time

############
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
########################################

broker_address="35.227.82.239"
print("creating new instance")
client = mqtt.Client("Test") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic","hydronizer/reports")
client.subscribe("hydronizer/reports")
print("Publishing message to topic","hydronizer/reports")
client.publish("hydronizer/reports","Test")
time.sleep(1000) # wait
client.loop_stop() #stop the loop
