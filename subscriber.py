import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
# print("%-15s %d %s" % (msg.topic, msg.qos, msg.payload.decode("utf-8")))
    print(msg.topic + " " + str(msg.payload.decode("utf-8")) + " " + str(msg.qos))

if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.subscribe("bees/#", 1)
    client.loop_forever()