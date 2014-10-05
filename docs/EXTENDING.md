# Extending the catflap camera

There are a lot of things you can do if you've got something that can tell you when the catflap is used. This is a non-exhaustive list of suggestions and examples of tools you can use.

## Messaging

The Pi is not a very powerful computer and the callback should be kept as quick as possible within the camera. You can make use of pub-sub messaging patterns to distribute messages about the catflap opening, for instance using Redis, RabbitMQ or ZeroMQ. This is a near-real-time way to distribute information, so can be used if you want to send an alert when your cat leaves or exits, control a light based on the cat's movements, etc.

## Recording video

The current catflap only records an image, which doesn't always tell the full story if the cat nudged the flap open before entering, for instance. The picamera library can [record video into a circular buffer](http://picamera.readthedocs.org/en/release-1.8/recipes1.html#recording-to-a-circular-stream) - try to write a modification to dump about 20 seconds of video, starting 5 seconds *before* the catflap was triggered.

## Streaming

With some reasonably simple modifications to the code you can stream encoded video (using the Pi's h264 encoder) to a server for distribution around a network. Ever wanted to check up on your catflap remotely? Now you can! Of course, it doesn't have to be a catflap - how about a bird feeder?

## ... and that's just the start of it

With the hardware for a catflap camera you can build all sorts of interesting and novel cameras. With a few more parts you can extend the camera to have control, too - how about a remote control dry food dispenser?

* [The Raspberry Pi website](http://www.raspberrypi.org/)
