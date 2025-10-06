import time
import pigpio
from RF24 import RF24, RF24_PA_LOW

# --- Pin configuration ---
TRIG = 26
ECHO = 19
CE_PIN = 22   # GPIO pin connected to CE of nRF24L01
CSN_PIN = 0   # SPI CE0 (usually 0)

# --- Setup radio ---
radio = RF24(CE_PIN, CSN_PIN)
address = b"00001"

# --- Setup pigpio ---
pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("pigpio daemon not running! Start it with: sudo pigpiod")

def setup():
    # Setup ultrasonic pins
    pi.set_mode(TRIG, pigpio.OUTPUT)
    pi.set_mode(ECHO, pigpio.INPUT)
    pi.write(TRIG, 0)

    # Setup nRF24L01
    if not radio.begin():
        raise RuntimeError("Radio hardware not responding")

    radio.setPALevel(RF24_PA_LOW)
    radio.openWritingPipe(address)
    radio.stopListening()
    print("RF24 Sender ready (pigpio distance version)!")

def getDistance():
    # Send 10µs pulse
    pi.gpio_trigger(TRIG, 10, 1)

    # Wait for echo start
    start = time.time()
    while pi.read(ECHO) == 0:
        start = time.time()

    # Wait for echo end
    end = start
    while pi.read(ECHO) == 1:
        end = time.time()

    duration = end - start
    distance = (duration * 17150)  # cm
    return round(distance, 2)

def loop():
    last_dist = None  # Last distance successfully sent

    while True:
        try:
            dist = getDistance()

            # Filter out invalid readings
            if dist > 300 or dist <= 0:
                print(f"Ignored invalid reading: {dist} cm")
                time.sleep(0.1)
                continue

            # Only send if first reading or change >= 10 cm
            if last_dist is None or abs(dist - last_dist) >= 10:
                message = f"{dist}".encode('utf-8')
                result = radio.write(message)

                if result:
                    print(f"Sent: {dist} cm (Δ={abs(dist - last_dist) if last_dist else 0:.2f})")
                else:
                    print("Send failed")

                last_dist = dist  # Update last sent distance
            else:
                print(f"No significant change (Δ={abs(dist - last_dist):.2f} cm)")

            time.sleep(0.1)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(0.5)



if __name__ == "__main__":
    setup()
    loop()
