import time
import serial

ard_kom = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

def podaci():
    dictionary = {}
    try:
        vrednosti = ard_kom.readline().decode("utf-8").rstrip('\r\n').split(',')
        dictionary['celzijus']=vrednosti[0]
        dictionary['vlaznost']=vrednosti[1]
        dictionary['co2_ppm']=vrednosti[2]
        return dictionary
    except KeyboardInterrupt:
        print("Kraj programa")


def celzijus():
    try:
        return ard_kom.readline().decode("utf-8").rstrip('\r\n').split(',')[0]
    except KeyboardInterrupt:
        print("Kraj programa")

def vlaznost():
    try:
        return ard_kom.readline().decode("utf-8").rstrip('\r\n').split(',')[1]
    except KeyboardInterrupt:
        print("Kraj programa")

def co2_ppm():
    try:
        return ard_kom.readline().decode("utf-8").rstrip('\r\n').split(',')[2]
    except KeyboardInterrupt:
        print("Kraj programa")