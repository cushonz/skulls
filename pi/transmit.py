import time
from RF24 import RF24, RF24_PA_LOW
import RPi.GPIO as GPIO

# Pin configuration for Raspberry Pi
CE_PIN = 22   # GPIO pin connected to CE of nRF24L01
CSN_PIN = 0   # SPI CE0 (usually 0)
radio = RF24(CE_PIN, CSN_PIN)

ECHO = 19
trig = 26

# Address must match Arduino receiver
address = b"00001"

def setup():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    if not radio.begin():
        raise RuntimeError("Radio hardware not responding")
    
    radio.setPALevel(RF24_PA_LOW)
    radio.openWritingPipe(address)
    radio.stopListening()  # Must stop listening for sending
    print("RF24 Sender ready!")

def getDistance():
    GPIO.output(trig, False)
    time.sleep(0.000012)

    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def loop():
    while True:
        dist = getDistance()
        message = f"{dist}".encode('utf-8')
        result = radio.write(message)
        
        if result:
            print(f"Sent: {message}")
        else:
            print("Send failed")
        
        time.sleep(1)  # Send every 1 second

if __name__ == "__main__":
    setup()
    loop()



