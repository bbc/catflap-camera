# Exploring the camera software

The Catflap Camera is a Python program which has lots of comments and is quite readable - first things first, go give the code a read! If you're unfamiliar with some of the constructs in the language, don't worry - you'll pick them up as you go, or can refer to some of the excellent language tutorials out there.

* [Learn Python The Hard Way](http://learnpythonthehardway.org/book/)
* [The Beginners Guide](https://wiki.python.org/moin/BeginnersGuide)
* [The Hitchhiker's Guide to Python](http://docs.python-guide.org/en/latest/)

This documentation aims to unpick the software and explain how it works, and some of the concepts behind the more complicated bits of code.

# Program Structure

![Program structure](http://www.gliffy.com/go/publish/image/6267342/L.png "Top-level diagram")

The general structure of the problem is pretty simple - our main program code doesn't do much, its job is to set up the camera and the GPIO (General Purpose Input/Output) handlers.

We first `import` some libraries. This basically asks Python to make these libraries available for our code to use.

Next we define a `Catflap` class; this is a collection of all our code. While we don't strictly speaking need to wrap all our code in a class, it's good practice to keep our code structured. It also lets us work with an *instance* of a class. An instance can store information about itself in variables; within the class we make reference to `self`, which is the current instance. We generally use this to store some context - what our class was set up with, information we need to keep track of across multiple method calls, and so on. For instance, we could write `self.foo = 'bar'`. Then in another method at another time we can call `self.foo` to retrieve `bar`.

The `__init__` method is called when we make a new *instance* of our class, which we'll do when we start the program. This method sets up our GPIO connector and camera LED. We also blink the LED in this method by calling a method we define below, which simply turns the LED on and off with a little delay between each change - this lets us see the program has started if we haven't got a computer connected to our Pi!

We also define a `catflap_callback` method; this is a *callback handler* which contains the code we want to run when something happens on our GPIO pin.

## Setting up GPIO

Let's look a little closer at our GPIO code

    GPIO.setup(self.switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

What are we actually doing here? Well, we're calling the setup method with a few arguments - `self.switch_pin` is just a reference to the pin we're using for our sensor, and it's set up a little bit further up. This is the pin we want to setup. The `GPIO.IN` argument is a variable that says we'd like to use the pin as an input - that is, we want to read a value from it.

Last but not least we enable what's called a *pull-up resistor* on the pin using the `pull_up_down=GPIO.PUD_UP` argument. This tells the chip to connect a resistor between the chip's power source and the pin.

Normally the pin wouldn't be connected to power or ground within the chip, and it would be what's referred to as *floating* - if we apply a voltage to it, it would read high, and if we grounded it, it would read low. In our case, we're using a switch, which doesn't apply either voltage or ground to this pin.

We need to give our pin two states so we can sense the switch changing; this is what the pull-up resistor does. If the pin is connected to an open circuit the pull-up resistor will *pull up* the voltage so our pin reads high. If the switch closes and connects the circuit to ground, the voltage will be pulled down to ground.

If we wanted to use external parts, we could build something like the below circuit schematic.

![Pull-up circuit diagram](https://github.com/JamesHarrison/catflap-camera/raw/master/docs/images/circuit_pullup.png "Example pull-up circuit")

However, this is a common enough task that the chip in the Raspberry Pi has internal components that can be configured to provide a pull-up function. This is what we're telling the chip to to do.

## Interrupts

When we're set up and ready to take a picture we could ask the program to check the pin and see if it's changed since it last looked. This is called *polling*. While we can do this, it has some drawbacks. We can't look at it all the time - we're going to need to go off and do other things. The Raspberry Pi's processor is single-threaded, so we can't guarantee that our polling loop will be looking at the pin all the time. What happens if the pin changes when we aren't looking?

Again, this is a common problem, and the chip has some helpful functionality which we can take advantage of. We can ask it to keep an eye on the pin in hardware. If the pin changes, it can send a message to our software (an *interrupt*, because it can interrupt what's going on at that moment in the CPU) and we can do something about it in software - we don't have to keep checking all the time.

    GPIO.add_event_detect(self.switch_pin, GPIO.BOTH,
                              callback=self.catflap_callback)

In this line of code we ask the GPIO library to add an interrupt monitoring our switch pin. We provide the callback, and specify the catflap_callback method we've defined as the method to call when an interrupt is triggered. When we say `GPIO.BOTH` we could also say `GPIO.RISING` or `GPIO.FALLING`. BOTH means we'll trigger on a rising or falling edge. When we talk about edges, we mean the transition between two voltages - when our pin goes from high to low (a fall) or low to high (a rise).

Looking at our method definition for the callback:

    def catflap_callback(self, pin):

We can see we only get told about *which* pin an event happened on - not about what state it is now (high or low). We could register a different function for a rising edge or a falling edge, but generally our events aren't happening that quickly, and we're not going to be overworking our Pi, so we'll just read the pin once we've been called:

    current_value = GPIO.input(pin)

Now we can check against this when we're making decisions about what to do:

    if current_value == GPIO.LOW:
        # do something!

## Debouncing

What happens when a cat goes through a catflap? Typically the flap will swing be pushed open, close mostly, the tail picks it back up again and then drops it, where it swings a couple of times until it stops. So for our cat coming in, we get maybe six or seven actual interrupts - so our function is called six or seven times.

We don't want to take six or seven pictures, just one - so we need to do a thing called *debouncing*. This is, as the name implies, a process by which we translate a number of related but disconnected digital signals into a single logical event and act on it. We usually have to do this even if the activation is relatively simple, like a button, because voltage levels are never quite perfect, and the chip might see two changes when only one occurred.

![Callback structure](http://www.gliffy.com/go/publish/image/6267293/L.png "Callback structure")

The easiest way to debounce a signal is to use time. When we start our program we make a note of what time it is - this timestamp is shared across all calls to the callback.

When the callback is called and we think about doing something we just check that timestamp. If it's more than a defined period - in our case, 2 seconds - we won't do anything, we'll just update our note about the last time we saw something happen. We assume that this is another event that's related to the last thing we did, and we can ignore it.

    if (time_now - self.time_stamp) >= 2:
        self.time_stamp = time_now

The timestamps - generated by a call to `time.time()` - that we're using are simply the number of seconds since the Unix epoch. That means we can subtract one from another, and get the number of seconds between the two times.

In our particular case, when the flap closes we don't mind repeating our action - which is simply to turn the LED off. So we don't have a separate debounce section for that part of the code.

## Threads

We've introduced the topic of threading rather slyly by using them without you perhaps noticing. Above, we mentioned that the hardware will interrupt whatever's going on so we know our catflap has done something. When we set up an *interrupt handler* we create a new thread of execution separate from our main thread.

This new thread sits around waiting for the operating system to pass on the interrupt and let it know something is happening, at which point it executes our callback. But this happens outside of our *main thread* - the thread we started off with. It's in a *child thread* - that's a thread which is spawned by the *parent*, our main thread. If the parent of a thread ends, all child threads end. Sounds a bit nasty but that's how Python works!

The result of this is that we need our main thread to stay alive, even if it doesn't do anything. This thread is just going to twiddle its thumbs while the callback thread does all the work! Let's look at our `run` method:

    def run(self):
        try:
            while True:
                time.sleep(0.1)
        finally:
            GPIO.cleanup()
            self.camera.led = False

Our `while True:` line creates an *intentional* infinite loop. Then we ask the program to go to sleep for 100 milliseconds (0.1 seconds). This tells the program to do nothing, in other words - just sleep.

Note however we've used this `try` block for this loop. We've also got a `finally` block below that - what's all that about? Well, if something goes wrong - let's say that the camera is shut down for some reason - we want to clean up after ourselves. Python will call the contents of a `finally` block once the `try` code has finished or crashed, no matter what.

# Kicking off our Catflap

We have some code below the class definition which will be run when the program is executed. Let's step through it!

    catflap_pin = 24

This just says which pin our catflap sensor is connected on.

    with picamera.PiCamera() as camera:

We're again using a block here - this asks the picamera library to give us a camera object we can use to take pictures. When the block is over, the camera will be released and closed for us.

        camera.resolution = (2592, 1944)
        camera.exif_tags['IFD0.Software'] = 'Catflap Camera v1.0'

Here we're setting the camera's resolution to its highest possible setting, and asking it to write an EXIF tag documenting the software that took the photo. EXIF tags are metadata which are stored in the headers of a picture; if you've ever wondered how you can upload a picture from a GPS enabled phone and have the website show you where you took it, or how the website knows what lens you were using, this is where that data's stored!

        catflap = Catflap(catflap_pin, camera)
        catflap.run()

This is where we kick off the main program. We create a new *instance* of our `Catflap` class, and store it in the `catflap` variable. This calls our `__init__` method implicitly, which sets up our interrupt handler and GPIO. Then we call the `run` method, which starts our infinite loop - and away we go!

# Logging

Throughout the program you can see references to `syslog` that look like this:

    syslog.syslog(syslog.LOG_INFO,
                   "I am a revision %s Raspberry Pi running RPi.GPIO %s"
                   % (GPIO.RPI_REVISION, GPIO.VERSION))

What does this do? Well, what this does is write a line like this to the system's log, or `syslog` for short.

    Oct  4 16:43:51 catflap camera.py[20868]: I am a revision 3 Raspberry Pi running RPi.GPIO 0.5.7

Notice that we get the current time, the hostname (catflap), the process name and ID (camera.py[20868]) and the string we wrote. What's all the % stuff about then? This is a technique called string interpolation.

Let's say we have a variable - for instance, `name`:

    name = 'Jas'

Now if we want to make a new string which says "Hello, (name)" we can do this:

    introduction = "Hello, %s" % name

We use the `%s` placeholder to say that we want to put a string here. We could use %d for a number - there's a range of options. If we want to interpolate multiple variables we do so like this:

    first_name = "John"
    last_name = "Smith"
    introduction = "Hello, %s %s" % (first_name, last_name)

Note we pass a list of parameters, wrapped in parentheses.

What's all the `syslog.LOG_INFO` about then? Well, this lets us set the priority of a message. We might want to make our logging very verbose to find out about problems, and then run it quietly to save disk space. INFO is, as the name implies, *informational*. We also use LOG_DEBUG for *debugging information*.

At the very start of the program we have to set up our logging, too.

    syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_DAEMON)

This asks the syslog library to *tag* our messages with the process identifier, and to send them to the *daemon facility*. This 'facility' is akin to a collection or group of related messages - in this case, the daemon facility relates to background processes. Perfect for our camera!
