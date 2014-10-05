# The Catflap Camera

The Catflap Camera is a simple Python script which uses a [Raspberry Pi](http://www.raspberrypi.org/help/what-is-a-raspberry-pi/), the add-on Raspberry Pi [camera board](http://www.raspberrypi.org/products/camera-module/) and a [reed switch](https://en.wikipedia.org/wiki/Reed_switch) sensor to take a picture when a catflap is used, thus capturing a lovely picture of whichever cat was using the catflap at the time.

The camera was used in the production of BBC Two's "Cat Watch 2014: The New Horizon Experiment". This repository is an open source version of the camera software, with instructions on how to build your own. Pull requests, suggestions and enhancements are welcomed!

![Demo](https://github.com/JamesHarrison/catflap-camera/raw/master/docs/images/entering.jpg "Cat entering through a camera-enabled catflap")

## What it is and how it works

The Pi sits next to your catflap, with the camera pointed at the catflap. A sensor (a reed switch) is mounted on the frame and flap, which basically flips a switch when a cat goes through. This gets noticed by the camera script on the Pi and the Pi takes a picture, which can be downloaded from the Pi using a web browser.

![Installation example](https://github.com/JamesHarrison/catflap-camera/raw/master/docs/images/example.jpg "An example of an installed camera")

# Making your own

You don't need to be an expert to build your own camera - the documentation assumes no prior knowledge of the Raspberry Pi hardware or software, but assumes you're familiar with computers.

* [Building the camera hardware](../master/docs/HARDWARE.md)
* [Installing and configuring the software](../master/docs/INSTALLATION.md)
* [Extending the software](../master/docs/EXTENDING.md)

# License

Copyright 2014 James Harrison

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this project except in compliance with the License. You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.