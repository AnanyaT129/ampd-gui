from time import sleep
import RPi.GPIO as GPIO
from gpiozero import LED

GPIO.setmode(GPIO.BCM)
onOffPin = 17
tds = LED(onOffPin)
GPIO.output(onOffPin, GPIO.LOW)
#tds.on()
GPIO.output(onOffPin, GPIO.HIGH)
print("pump on")

sleep(5)
#tds.off()
GPIO.output(onOffPin, GPIO.LOW)
print("pump off")
