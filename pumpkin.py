import pigpio
import time
import rpi_ws281x
import random
import threading


# Set up the pigpio library.
pi = pigpio.pi()

# Define the pins.
pwm_fan_control_pin = 13
hall_effect_pin = 23
mister_pin = 26

rot =0

def rotation(GPIO, level, tick):
    global rot

    if level == 1:
        print("rot: ", rot)
        rot +=1


hall_count = pi.callback(hall_effect_pin)

# Turn off all the pins
pi.set_PWM_dutycycle(mister_pin, 0)
pi.set_PWM_dutycycle(pwm_fan_control_pin, 0)

# LED strip configuration:
LED_COUNT      = 180      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# Create NeoPixel object with appropriate configuration.
strip = rpi_ws281x.Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).

strip.begin()

def pixel_clear():
    # Clear all the pixels
    for i in range(strip.numPixels()):  # Green Red Blue
        strip.setPixelColor(i, rpi_ws281x.Color(0, 0, 0))

strip.show()


class PixelShow(threading.Thread):

    def __init__(self, strip, wait=0.1):
        super(PixelShow, self).__init__()
        self.strip = strip
        self.wait = wait
        print("Pixel show thread")

    def run(self):

        while True:

            for pix in range (0, 180):
                # determine if off or on and then multiply by a brightness
                self.strip.setPixelColor(pix, rpi_ws281x.Color(random.randint(0,1) * random.randint(0,255), 0, 0))
            self.strip.show()

            time.sleep(self.wait)


pixel_thread = PixelShow(strip, 0.08)

pixel_thread.start()


try:

    print("Press Ctrl-C to finish")

    pixel_clear()

    # main loop
    while True:


        for value in range (20, 72, 10):

            # mister full on.
            pi.set_PWM_dutycycle(mister_pin, 255)


            # Wait for a few seconds to let mist build
            time.sleep(10)

            #for y in range(1, 50):
            #    strip.setPixelColor(random.randint(0,179), rpi_ws281x.Color(random.randint(0,255), 0, 0))
            #strip.show()

            print("PWM: ", value)

            # fan on for a bit and then off again to complete cycle
            pi.set_PWM_dutycycle(pwm_fan_control_pin, int(float(value/100) *255))

            time.sleep(4)

            # fan on for a bit and then off again to complete cycle
            pi.set_PWM_dutycycle(pwm_fan_control_pin, 0)

            time.sleep(2)



except KeyboardInterrupt:
    print("Control-C received")

# Clean up to finish -important to turn pins off.
finally:
    print("final cleanup")
    pi.set_PWM_dutycycle(mister_pin, 0)
    pi.set_PWM_dutycycle(pwm_fan_control_pin, 0)

    #pi.hardware_PWM(pwm_fan_control_pin, 25000, 0)
    pi.stop()

    pixel_clear()

    #unicornhat.off()
