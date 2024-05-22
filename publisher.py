import paho.mqtt.publish as publish
import skripta
import time

host = "localhost"

if __name__ == '__main__':
# publish a single message
    while True:
        msgs=[{'topic': "bees/celzijus", 'payload': skripta.celzijus() },
        {'topic': "bees/vlaznost", 'payload': skripta.vlaznost()},
        {'topic': "bees/co2_ppm", 'payload': skripta.co2_ppm()},]
        publish.multiple(msgs, hostname=host)
        time.sleep(0.1)