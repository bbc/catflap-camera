
# Hardware for the Camera

## Required Components

To run the Catflap Camera as-is, you will need the following:

* **Raspberry Pi Model B or B+** and SD/uSD card (eg [2431427](http://uk.farnell.com/raspberry-pi/raspberry-modb-8gb-usd/raspberry-pi-model-b-8gb-noobs/dp/2431427))
* **Raspberry Pi Camera Board** (optionally NoIR) (eg [2357308](http://uk.farnell.com/raspberry-pi/rpi-noir-camera-board/raspberry-pi-noir-camera-board/dp/2357308))
* **1A/5V microUSB power supply**
* A **reed switch** and **magnet** (eg [2218016](http://uk.farnell.com/jsp/search/productdetail.jsp?CMP=i-ddd7-00001003&sku=2218016) / [607230](http://uk.farnell.com/jsp/search/productdetail.jsp?CMP=i-ddd7-00001003&sku=607230))

All of the above items can be found at Farnell (order codes are listed above) but can also be found at most online component retailers, such as RS or Maplin.

![Installation example](https://github.com/JamesHarrison/catflap-camera/raw/master/docs/images/example.jpg "An example of an installed camera")

## Connecting the sensor

The sensor should be connected between **GPIO input pin 24** and **any of the Raspberry Pi's ground pins**. It doesn't matter which wire is connected to which pin (polarity) - switches have no polarity.

While it is possible to connect the sensor to the Pi without soldering, it is considerably easier if you have access to a soldering iron. Most reed switches have short wires that require extending to reach the Pi; additionally, the Pi has 0.1mm pitch header pins to connect to. As such you'll probably want to purchase some 0.1mm jumpers, some single or two-core wire, a soldering iron and some solder if you do not have this already.

Alternatively, you can purchase screw terminal add-ons for the Raspberry Pi which when combined with a reed switch featuring long terminal leads can provide a solder-free solution. However, this does add some cost which can be avoided if you already have access to the required parts.

## Sensors

We chose a reed switch for its ease of use and simplicity of installation. The switch is configured so that it is held open by the magnet when the flap is closed. The magnet is mounted on the flap; the switch is mounted as close as possible to the magnet without impeding the flap. When the flap opens, the magnet moves away, the switch triggers and the circuit opens, allowing the Raspberry Pi's pull-up resistors to pull the line high.

Any sensor can be used so long as it follows this mode of operation - when the flap is open the switch is open (current cannot pass), when the flap is closed the switch is closed. The camera contains debouncing logic to prevent multiple activations from a swinging flap settling.

### Mounting the reed switch

The sensor we used for the Horizon programme, listed above, is very small, making it easy to embed into the frame of a catflap without impeding the flap. On most flaps it can simply be taped in place, or held in place with some blu-tak. Ensure that there's no exposed adhesive that could stick to the cat!

The magnet is taped, using a strong Gaffer tape, to the flap; PVC (electrician's) tape will also work well. Make sure that no adhesive is left exposed, and that the magnet is secure. 

If you're installing the magnet permanently, use tape while you test that the sensor works properly. Once you're happy with the alignment, use cyanoacrylate (superglue) or hot melt glue to secure the magnet permanently. Use a layer of tape to enclose the entire glued assembly - this will help keep it from sticking to or catching the cat. Make sure the glue is fully dry before the cat is allowed to use the flap.

## The Camera

We use the Raspberry Pi camera board as it avoids a lot of the complexity associated with USB webcams and other plug-in camera solutions. It also provides us with a very simple interface (a single LED) and excellent high resolution images out of the box.

Mounting the camera can be done with double-sided tape or using a case designed for the camera board. Most of our installations for the series used blu-tak and tape, which was entirely sufficient to secure the board.

While no dangerous voltages are exposed in the camera board, if your home contains very curious cats, dogs or toddlers then you should consider purchasing or making a more robust case to house the camera and Raspberry Pi.

The camera has a wide field of view but needs to be set back about 40 centimetres from the catflap to focus properly.
