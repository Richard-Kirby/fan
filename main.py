import pigpio
import time
import rpi_ws281x
import random

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


#pi.hardware_PWM(pwm_fan_control_pin, 25000, 0)


hall_count = pi.callback(hall_effect_pin)

# Turn off all the pins
pi.set_PWM_dutycycle(mister_pin, 0)
pi.set_PWM_dutycycle(pwm_fan_control_pin, 0)



#import unicornhat
#unicornhat.set_layout(unicornhat.PHAT)
#unicornhat.set_pixel(0, 0, 255, 255, 255)
#unicornhat.set_pixel(0, 1, 255, 255, 255)
#unicornhat.set_pixel(0, 2, 255, 255, 255)
#unicornhat.set_pixel(0, 3, 255, 255, 255)

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

for i in range(strip.numPixels()):  # Green Red Blue
    strip.setPixelColor(i, rpi_ws281x.Color(0, 0, 0))

strip.show()

#unicornhat.show()

try:

    print("Press Ctrl-C to finish")


    # Keep cycling through various colours - assume the user will press Control-C to finish.
    while True:

        # Turn green on 100% for a couple of seconds and the off,
        #pi.set_PWM_dutycycle(pwm_control_pin, 255)
        #print("fan 100%")
        #time.sleep(3)
        #pi.set_PWM_dutycycle(pwm_control_pin, int(255 / 10))
        #print("fan 10%")
        #time.sleep(3)

        # Cycle through the top ends of value and saturation and through the different colours
        for value in range (20, 102, 2):
            #pi.set_PWM_dutycycle(mister_pin, int(255 * float(value/100)))

            # mister full on.
            pi.set_PWM_dutycycle(mister_pin, 255)


            #pi.hardware_PWM(pwm_fan_control_pin, 25000, value * 10000)

            for y in range(1, 50):
                strip.setPixelColor(random.randint(0,179), rpi_ws281x.Color(random.randint(0,255), 0, 0))

            strip.show()

            pi.set_PWM_dutycycle(pwm_fan_control_pin, int(255 * float(value/100)))

            print("PWM: ", value)

            '''
            count = 0

            
            for i in range(1,400):

                hall_state = pi.read(hall_effect_pin)

                if hall_state == 0:
                    count = count + 1
                    print("C:", count)

                time.sleep(0.1)
            '''
            time.sleep(5)

            print(hall_count.tally())
            hall_count.reset_tally()

except KeyboardInterrupt:
    print("Control-C received")

# Clean up to finish -important to turn pins off.
finally:
    print("final cleanup")
    pi.set_PWM_dutycycle(mister_pin, 0)
    pi.set_PWM_dutycycle(pwm_fan_control_pin, 0)

    #pi.hardware_PWM(pwm_fan_control_pin, 25000, 0)
    pi.stop()
    #unicornhat.off()
