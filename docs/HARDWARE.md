
# Hardware for the Camera

## Required Components

To run the Catflap Camera as-is, you will need the following:

* **[Raspberry Pi](http://www.raspberrypi.org/products/model-b-plus/) Model B or B+** and SD/uSD card
* **[Raspberry Pi Camera Board](http://www.raspberrypi.org/products/camera-module/)** (optionally [NoIR](http://www.raspberrypi.org/products/pi-noir-camera/))
* **SD/microSD card** (micro SD for B+, otherwise SD; class 10 recommended; at least 4GB, 16GB recommended)
* **1A/5V microUSB power supply**
* A **reed switch** and **magnet**

You can locate all of the above parts through hobbyist and professional electronics shops, both online and in brick-and-mortar stores. Reed switches are commonly used in building intruder alarms to detect doors opening, so you can sometimes find them in home improvement stores.

![Components ready to go](https://github.com/JamesHarrison/catflap-camera/raw/master/docs/images/pi_cam_prebuild.jpg "A Pi and camera ready to begin")

The total cost of hardware is around £65 including shipping. If you need to purchase a soldering iron and other items you can expect to spend up to £110 (assuming entry-level parts).

![Installation example](https://github.com/JamesHarrison/catflap-camera/raw/master/docs/images/example.jpg "An example of an installed camera")

## Safety

The catflap camera was designed to put the safety of the cat first and foremost; as such it is non-invasive, doesn't require a collar or microchipping, and is made from parts that are inherently safe.

While no dangerous voltages are exposed in the camera board, if your home contains very curious cats, dogs or toddlers then you should consider purchasing or making a more robust case to house the camera and Raspberry Pi. Suitable cases can be bought for a few pounds from most online retailers.

Because the assembly process involves glue and potentially a soldering iron, adult supervision is advised.

## Raspberry Pi essentials

You'll need to provide a network connection to your Raspberry Pi. This is because the Pi needs a way to find out what date and time it is so that it can 'timestamp' the pictures it takes. If the pictures all claim to have been taken in 1970 it's because the Pi isn't able to find out what time it is.

If your catflap is near your network router or switch then you should simply run a Cat5/Cat6 cable from the router to the Pi. This is the simplest and cheapest option.

If your catflap is further away from your router you'll need to use a USB wireless dongle. These can be bought for around £15 and plug into a USB port on the Pi.

You'll also need a keyboard and mouse to configure your Pi, and a HDMI cable to plug the Pi into your television. You can perform configuration tasks using a terminal accessed with a 3v3 serial port cable, which requires only another computer rather than a full television/keyboard/mouse setup. Likewise once your Pi is on the network you can access it remotely from another PC. How to configure all of this is out of scope for this documentation.

General help on how to configure your Raspberry Pi can be found [on the Raspberry Pi website](http://www.raspberrypi.org/help/).

## Connecting the sensor

The sensor should be connected between **GPIO input pin 24** and **any of the Raspberry Pi's ground pins**. It doesn't matter which wire is connected to which pin (polarity) - switches have no polarity. The only important thing is that the two wires are normally open (if you put a multimeter in resistance measurement mode across the poles, you should see infinite resistance when the magnet is present and near-zero resistance when the magnet is absent).

While it is possible to connect the sensor to the Pi without soldering, it is considerably easier if you have access to a soldering iron. Most reed switches have short wires that require extending to reach the Pi; additionally, the Pi has 0.1mm pitch header pins to connect to. As such you'll probably want to purchase some 0.1mm jumpers, some single or two-core wire, a soldering iron and some solder if you do not have this already.

![Soldering a sensor lead](https://github.com/JamesHarrison/catflap-camera/raw/master/docs/images/sensorsoldering.jpg "Soldering a sensor lead to a 0.1\" header")

Alternatively, you can purchase screw terminal add-ons for the Raspberry Pi which when combined with a reed switch featuring long terminal leads can provide a solder-free solution. However, this does add some cost which can be avoided if you already have access to the required parts.

![A Pi wired up](https://github.com/JamesHarrison/catflap-camera/raw/master/docs/images/pi_wired.jpg "The pi wired up")

## Sensors

We chose a reed switch for its ease of use and simplicity of installation. The switch is configured so that it is held open by the magnet when the flap is closed. The magnet is mounted on the flap; the switch is mounted as close as possible to the magnet without impeding the flap. When the flap opens, the magnet moves away, the switch triggers and the circuit opens, allowing the Raspberry Pi's pull-up resistors to pull the line high.

Any sensor can be used so long as it follows this mode of operation - when the flap is open the switch is open (current cannot pass), when the flap is closed the switch is closed. The camera contains debouncing logic to prevent multiple activations from a swinging flap settling.

![Soldering a sensor lead](https://github.com/JamesHarrison/catflap-camera/raw/master/docs/images/sensor.jpg "An example sensor with lead soldered")


### Mounting the reed switch

The reed switch we used for the Horizon programme is very small, making it easy to embed into the frame of a catflap without impeding the flap. On most flaps it can simply be taped in place, or held in place with some blu-tak. Ensure that there's no exposed adhesive that could stick to the cat!

The magnet is taped, using a strong Gaffer tape, to the flap; PVC (electrician's) tape will also work well. Make sure that no adhesive is left exposed, and that the magnet is secure. 

If you're installing the magnet permanently, use tape while you test that the sensor works properly. Once you're happy with the alignment, use cyanoacrylate (superglue) or hot melt glue to secure the magnet permanently. Use a layer of tape to enclose the entire glued assembly - this will help keep it from sticking to or catching on the cat. Make sure the glue is fully dry and tack-free before the cat is allowed to use the flap!

## The Camera

We use the Raspberry Pi camera board as it avoids a lot of the complexity associated with USB webcams and other plug-in camera solutions. It also provides us with a very simple interface (a single LED) and excellent high resolution images out of the box.

Mounting the camera can be done with double-sided tape or using a case designed for the camera board. Most of our installations for the TV series used blu-tak and tape, which was entirely sufficient to secure the board.

The camera has a wide field of view but ideally needs to be set back about 40 centimetres from the catflap to focus properly.

### Lighting (standard vs NoIR boards)

If you want your camera to work through the night as well as the day, you'll need to provide some lighting near the catflap. This can take the form of a small nightlight or desk light. You can also purchase LED light modules specifically designed to be used with the Pi camera, or you can make your own LED illuminator with some LEDs, some solder and some glue or cardboard.

Alternatively, if you want to avoid having lights on and visible all night, you can use the Raspberry Pi NoIR camera board, which has no infrared filter. This will need to be kept out of direct sunlight to avoid being washed out. 

The NoIR board lets you use infrared illuminators, which are commonly used for security cameras and can be purchased for around £25 from security and electronics suppliers. However, colours with the NoIR will be 'off' - things will appear slightly purple and the scene will look a bit odd in terms of intensities.

## Catflaps

Your catflap must allow a sensor to be mounted almost in contact with the flap itself, and for a magnet to be attached to the flap with tape/glue.

If your flap is recessed into a door or wall you may not be able to fit a reed switch sensor as it will impede the frame. In this case you may have to evaluate other sensors. If your sensor will be normally closed, you can invert the logic in software to work around this by replacing references to GPIO.HIGH with GPIO.LOW and vice versa in `camera.py`.

