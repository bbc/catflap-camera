# Raspberry Pi Catflap Camera
# Copyright 2014 BBC Research & Development

## -- Scary license boilerplate --
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
## -- That's it for scary licenses. Let's code! --

import time
import sys
import syslog

# Open syslog for logging
syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_DAEMON)

# Import the RPi.GPIO library
try:
    import RPi.GPIO as GPIO
except Exception:
    # If we don't have it, explain how to install it
    syslog.syslog(syslog.LOG_INFO,
                  "Error importing RPi.GPIO - you may need to install this "
                  "library (pip install RPi.GPIO) or run this script "
                  "with superuser privs")
    sys.exit(255)

# Import the picamera library
try:
    import picamera
except Exception:
    # If we don't have it, explain how to install it
    syslog.syslog(syslog.LOG_INFO,
                  "Error importing picamera - you may need "
                  "to install this library (pip install picamera) or run this "
                  "script with superuser privs ")
    sys.exit(255)


class Catflap(object):
    """
    This is the Catflap class. All of the catflap specific code lives in here!
    """

    def __init__(self, switch_pin, camera):
        """
        Called when the Catflap is set up. Needs the pin number (in Broadcom
        terms) the sensor is wired to, and an instance of PiCamera.
        """
        # Parrot out some useful facts to syslog
        syslog.syslog(syslog.LOG_INFO,
                      "I am a revision %s Raspberry Pi running RPi.GPIO %s"
                      % (GPIO.RPI_REVISION, GPIO.VERSION))
        syslog.syslog(syslog.LOG_INFO,
                      "Catflap sense lead should be connected to P1-%i"
                      % catflap_pin)

        # Set our debounce timer to an initial value that makes sense
        self.time_stamp = time.time()

        # Set our GPIO library to use RPi board pin numbering
        GPIO.setmode(GPIO.BCM)

        # Make a note of the pin we're using
        self.switch_pin = switch_pin
        self.camera = camera

        # Turn off the LED
        self.camera.led = False
        # Blink our LED a few times to say we've woken up!
        self.blink()

        # Set up the catflap pin as an input, and configure the internal
        # pull-up resistors to pull the pin high.
        GPIO.setup(self.switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Set up an interrupt handler for both rising and falling edges
        GPIO.add_event_detect(self.switch_pin, GPIO.BOTH,
                              callback=self.catflap_callback)

    def blink(self):
        """
        Blink the camera LED on and off a few times
        """
        for iter in range(0, 6):
            self.camera.led = True
            time.sleep(0.1)
            self.camera.led = False
            time.sleep(0.1)

    def catflap_callback(self, pin):
        """
        This function is called by the RPi.GPIO library when an interrupt
        occurs, set up by the add_event_detect call in __init__.

        Interrupts are very efficient compared to polling for low latency
        applications - we don't want delay between the cat appearing and
        the shutter on the camera!
        """
        # When was the interrupt triggered?
        time_now = time.time()
        # Read and store the current state of the pin - high or low
        current_value = GPIO.input(pin)
        # Log the event
        syslog.syslog(syslog.LOG_DEBUG,
                      "GPIO event (%s) - time_now %s, last activation at %s"
                      % (GPIO.input(pin), time_now, self.time_stamp))
        if current_value == GPIO.LOW:
            # If the pin is low, the flap is closed!

            # Turn off the camera LED
            self.camera.led = False

            # Take a note
            syslog.syslog(syslog.LOG_DEBUG, "Flap closed at %s" % time.time())

        elif current_value == GPIO.HIGH:
            # If the pin is high, the flap has opened!
            # But it might be the case that we already saw the flap open and
            # what we're actually seeing is the flap swinging past the sensor
            # as it settles back down to close. Let's check!
            syslog.syslog(syslog.LOG_DEBUG, "Flap opened at %s" % time.time())
            if (time_now - self.time_stamp) >= 2:
                # If it's been two seconds since we last saw a flap open event
                # then we're interested in this one as a new event

                # Let's store the time this event happened
                self.time_stamp = time_now

                # Log it!
                syslog.syslog(syslog.LOG_INFO, "Taking a picture of a cat!")

                # We're going to turn on the camera light
                self.camera.led = True

                # Now we generate a filename based on the time, for instance
                # 20141007-200000.jpg (8pm Oct 7th 2014). This means we can
                # easily find out when a specific photo was taken!
                filename = "%s.jpg" % time.strftime("%Y%m%d-%H%M%S")
                # Now we prepend the filename with the path we're using
                # to store all our photos - in this case, /srv/cats
                final_path = "/srv/cats/%s" % filename

                # We're using the camera instance given to the class initially
                # which is being held open and ready for us - all we need
                # to do is ask it to capture an image to a path.
                # We configure the camera when we set up this class below.
                self.camera.capture(final_path)

                # Let syslog know for debugging purposes
                syslog.syslog(syslog.LOG_DEBUG, "Captured image %s at %s"
                              % (filename, time_now))
            else:
                # If it's been less than two seconds since the last cat,
                # this is probably just the flap swinging past the sensor

                # But keep a record to help us figure out problems
                syslog.syslog(syslog.LOG_INFO, "Debounce filtered an event")


    def run(self):
        """
        This method is called to stop the program exiting while we wait for
        our interrupt to trigger the callback. The callback is executed in
        another thread of execution so we don't have to do anything here but
        wait; we'll also clean up if we're terminated
        """
        try:
            while True:
                time.sleep(0.1)
        finally:
            GPIO.cleanup()
            self.camera.led = False

# The pin we've got the sensor connected to. We assume the other side of the
# sensor is connected to a ground pin - it doesn't matter which one.
catflap_pin = 24


# This gets a camera handle and holds it open for us.
# This means we don't spend time when we need to take a picture waiting for
# the camera to be initialized - we can take pictures near-instantly.
with picamera.PiCamera() as camera:

    # We set the camera resolution to its highest setting - downscaling is done
    # in software, so this is actually easiest.
    camera.resolution = (2592, 1944)
    # We can set EXIF tags here - record what camera model we are
    camera.exif_tags['IFD0.Software'] = 'Catflap Camera v1.0'
    # Set up a new instance of the catflap, providing the pin and camera
    catflap = Catflap(catflap_pin, camera)
    # Run the catflap - this will run forever or until it is killed by
    # entering Ctrl+C at the prompt, or by a term/kill signal
    catflap.run()
