import time
import RPi.GPIO as GPIO  # Import RPi.GPIO module
from time import sleep

from hal import hal_led as led
from hal import hal_input_switch as switch

# Define `flag` as a global variable
flag = False

def init():
    GPIO.setmode(GPIO.BCM)  # Choose BCM mode
    GPIO.setwarnings(False)
    GPIO.setup(22, GPIO.IN)  # Set GPIO 22 as input
    GPIO.setup(24, GPIO.OUT) # Set GPIO 24 as output

def read_slide_switch():
    ret = 0
    if GPIO.input(22):
        ret = 1
    return ret

def led_blink():
    GPIO.output(24, 1)
    time.sleep(0.05)
    GPIO.output(24, 0)
    time.sleep(0.05)

def led_blink_right():
    global flag  # Access the global `flag` variable
    if not flag:
        start_time = time.time()
        while time.time() - start_time < 5:  # Blink for 5 seconds
            led_blink()
        flag = True  # Set `flag` to True after blinking
    GPIO.output(24, 0)

def led_blink_left():
    global flag  # Access the global `flag` variable
    GPIO.output(24, 1)
    time.sleep(0.5)
    GPIO.output(24, 0)
    time.sleep(0.5)
    flag = False  # Set `flag` to False after blinking

def main():
    init()  # Initialize GPIO settings
    try:
        while True:  # Continuous loop to monitor switch state
            if read_slide_switch() == 1:
                led_blink_left()
            else:
                led_blink_right()
            time.sleep(0.1)  # Small delay to reduce CPU usage
    except KeyboardInterrupt:
        GPIO.cleanup()  # Cleanup GPIO on exit

# Main entry point
if __name__ == "__main__":
    main()
