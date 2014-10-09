# Installing the camera

A brief note on style conventions in this document - things you can type in to your Pi or will see on the console are written `like this`.

## Hardware Preparation

* Connect the Raspberry Pi camera to the Pi's camera socket - [check the orientation of the cable is correct](http://www.raspberrypi.org/documentation/configuration/camera.md) (blue backing towards the ethernet port)
* Plug in your HDMI cable between a port on your television or monitor and the Pi
* Connect your keyboard and mouse
* Plug in your USB wireless dongle or network cable

![The Pi wired up and ready to go](https://github.com/JamesHarrison/catflap-camera/raw/master/docs/images/pi_wired.jpg "The Pi ready to be configured")

Once you've got your Pi wired up, you need to plug in an SD card with an operating system. The [NOOBS](http://www.raspberrypi.org/help/noobs-setup/) card is designed for first-time users of the Raspberry Pi, and we'll assume you're using this. The end goal is a Raspbian Linux installation, so if you're familiar with the Pi you can skip ahead!

Once you have the SD card (or microSD for the B+) set up, plug it into the Pi and connect your power supply to the Pi. You'll see the NOOBS boot screen. Select Raspbian when prompted and press install. Wait for a bit (you'll probably want to go and make a cup of tea) until it's finished. It'll then reboot into Raspbian.

### Pre-built image

If you're happy working with a pre-configured image if it doesn't work, you can download an 8GB (compressed to 2.5GB) SD card image based on NOOBS with all of the below configuration steps performed and the camera set to start on boot. All you need to do is [write the image to a card](http://www.raspberrypi.org/documentation/installation/installing-images/README.md), plug it in, connect the sensor and turn it on. The card must be at least 8GB.

You can download the image [here](https://assets.talkunafraid.co.uk/catflap-2014-10-05.img.bz2) (2.4GB).

You'll still need to [configure your wireless network](http://www.raspberrypi.org/documentation/configuration/wireless/README.md) if you can't use an ethernet cable, and should log in and change the password (by default it's `raspberry`, username `pi`).

Once you've connected it to your network via an ethernet cable you can log into it using a SSH client and the hostname `catflap.local`. You can view pictures it's taken by visiting `http://catflap.local/` in a web browser.

## Configuring Raspbian

When the Pi finishes booting up, you'll be dropped into the `raspi-config` tool. This lets you configure some basic system settings. If you need to get back to it at any time, run `sudo raspi-config`.

Your filesystem is already expanded if you're using NOOBS. You should change your user password (by default it's `raspberry`) to something only you know.

Crucially you need to select `5. Enable Camera` and select `Enable`.

We also recommend you overclock your Raspberry Pi using the Medium setting. This will help to speed up your Pi.

Select `Finish` and answer `Yes` when prompted to reboot now.

### Updating the system

Once the Pi has booted up again, log in and run `sudo rpi-update` to upgrade to the latest firmware, then run `sudo apt-get update && sudo apt-get upgrade` to upgrade the operating system packages. Reboot again once it's all done - it'll take a little while, so go make a cup of tea or read through some of the Raspberry Pi documentation on their website while you wait.

### Disabling the camera LED

Last but not least we need to disable the camera LED - we'll control this manually. This command will append the appropriate setting to the Raspberry Pi's configuration file:

    sudo sh -c 'echo "disable_camera_led=1" >> /boot/config.txt'

Once this is done, reboot the Pi for the change to stick.

### Remote Access

You can do practically all of the subsequent tasks (and indeed the above tasks) from another computer on the network once your Pi is on your home wifi or wired connection. Use an SSH client (try [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/) for Windows) from another computer to connect to the IP address of the Raspberry Pi, and log in with the username `pi` and password specified earlier (by default `raspberry` if you didn't change it yet).

If you've plugged in your Pi to a wired connection then you don't need to do anything else. If you're using a USB wi-fi dongle, [follow these instructions](http://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md) to configure your Pi's wireless network adapter.

To find your Pi's IP address, simply enter `ip addr`.

    pi@catflap ~ $ ip addr
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
           valid_lft forever preferred_lft forever
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
        link/ether b8:27:eb:c8:db:46 brd ff:ff:ff:ff:ff:ff
        inet 10.0.0.224/24 brd 10.0.0.255 scope global eth0
           valid_lft forever preferred_lft forever
    3: wlan0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN qlen 1000
        link/ether 80:1f:02:6c:71:fc brd ff:ff:ff:ff:ff:ff

In the above example you can see under eth0 (our wired connection) an inet address of `10.0.0.224`. This is the IP address our Pi has been given on the local network. There's also an address `127.0.0.1` given; this is for the `lo` or 'loopback' interface - this isn't what you want.

This IP address may change - your router may have the ability to reserve an address for the Pi, or you can use Zeroconf to have the Pi announce itself on the network for easy discovery, removing the need to use IP addresses directly entirely.

### Installing a Zeroconf daemon

It's fiddly mucking around with IP addresses - there's a solution at hand, though. Using the Zeroconf/mDNS protocol we can advertise the Pi on the network.

* Install avahi: `sudo apt-get install avahi-daemon`

That's it! You may want to change the hostname of the pi with `raspi-config`. For instance, if you set the hostname to `catflap` and restart, you can put `http://catflap.local` in a browser or SSH to `catflap.local` instead of using the IP address. By default the hostname is `raspberrypi`, so you'd use `raspberrypi.local`

## Preparing for the camera software

First, let's try taking a picture. Run `raspistill -o test.jpg`. If you've got a monitor plugged in, even without a desktop environment, you'll see a preview before the picture is taken. If something isn't working here you'll need to fix that before proceeding - you may not have enabled the camera in `sudo raspi-config`, or you might not have rebooted since you did so.

You also shouldn't see a camera LED light up as a picture is taken. If you do, go back and disable the LED and then restart the Pi.

### Installing a webserver

When we've set up the camera in situ we probably won't have it plugged into a screen. We'll need a way to view these pictures from another computer. The simplest way is to run a web server on the Raspberry Pi - this will let us download and view the pictures in any web browser from any device on the network. We'll install nginx, a common lightweight web server, and configure it to serve images from a `/srv/cats` folder.

* Update apt's repositories: `sudo apt-get update`
* Install nginx: `sudo apt-get install nginx-light`
* Make the folder: `sudo mkdir -p /srv/cats`
* Make sure we can write to it: `sudo chmod 665 /srv/cats`
* Disable the default configuration: `sudo rm -rf /etc/nginx/sites-enabled/default`
* Make our server configuration: `sudo nano -w /etc/nginx/sites-enabled/cats`

This last command opens the `nano` editor. Write the following configuration, then press `Ctrl+O` to write the file and `Ctrl+X` to close nano.

    server {
       listen 80;
       root /srv/cats;
       location / {
            autoindex on;
       }
    }

Finally we need to restart nginx with `sudo service nginx restart`. You should now be able to visit `http://pi-ip-or-hostname.local/` and see a web page. No pictures yet, but not to worry! Let's take a picture to that folder:

        sudo raspistill -o /srv/cats/test.jpg

Reloading the page in your browser will now show you a file, `test.jpg`. Click on that and you can see the picture you just took!

![Webserver demo](https://github.com/JamesHarrison/catflap-camera/raw/master/docs/images/catflap-webserver.png "The webserver")

We can now take pictures and see them. This can be a lot of help when checking the camera placement. If you've got remote access, now would be a good time to move the Pi and camera to its final position.

### Installing Python dependencies

The camera software relies on a few Python libraries we have to install before we can install the camera software.

* Install picamera: `sudo apt-get install python-picamera`

The RPi.GPIO library is already installed by default on Raspbian, but if you need to install it, or need to upgrade it:

* Install pip: `sudo apt-get install python-pip`
* Install RPi.GPIO: `sudo pip install RPi.GPIO --upgrade`

## Connecting the sensor

Connect your reed switch to [pin 24](http://pi.gadgetoid.com/pinout/pin18_gpio24) and a [ground pin](http://pi.gadgetoid.com/pinout/pin20_ground) on the Pi's GPIO interface. You can find out which physical pins on the Raspberry Pi this relates to on the excellent [Pinout](http://pi.gadgetoid.com/pinout) website.

## Installing the camera

Now we're ready to actually install the camera script! Let's get a copy of the code. We won't install it in our home directory as we need to run this on boot.

* Install git: `sudo apt-get install git`
* Checkout the code: `sudo git clone https://github.com/JamesHarrison/catflap-camera.git /opt/catflap-camera`

Now we've got the camera installed we can run it. Let's do that to test it's working.

Run it with `sudo python /opt/catflap-camera/camera.py`. You won't see any output - that's normal. Try moving the magnet around your sensor to trigger the camera. Give it a minute or so of this and look at your web server - you should see some pictures! You can enter `Ctrl+C` to turn off the camera and return to your prompt.

If things aren't working (or even if they are) you'll probably want to look at the system log, where messages from the camera will be recorded. You can use a couple of appropriately named standard tools called `cat` and `tail` to inspect them.

`cat /var/log/syslog` will print the entire log to your console. This probably isn't useful. You can pass it through the `grep` filter to just look for lines about the camera - `cat /var/log/syslog | grep camera` will yield something like the below log extract.

We can use `tail` to get a subset of a file starting at the end of the file (there's another utility, `head`, which is the same but starts from the beginning of a file). `tail -n 50 /var/log/syslog` will only print the last 50 lines of a log, and can be combined with `grep` for filtering.

    Oct  4 16:43:51 catflap camera.py[20868]: I am a revision 3 Raspberry Pi running RPi.GPIO 0.5.7
    Oct  4 16:43:51 catflap camera.py[20868]: Catflap sense lead should be connected to P1-24
    Oct  4 16:44:04 catflap camera.py[20868]: GPIO event (0) - time_now 1412441044.84, last activation at 1412441031.27
    Oct  4 16:44:04 catflap camera.py[20868]: Flap closed at 1412441044.84
    Oct  4 16:44:04 catflap camera.py[20868]: GPIO event (1) - time_now 1412441044.89, last activation at 1412441031.27
    Oct  4 16:44:04 catflap camera.py[20868]: Flap opened at 1412441044.89
    Oct  4 16:44:04 catflap camera.py[20868]: Taking a picture of a cat!

You can use `tail -f /var/log/syslog` to follow a log file - this is very useful when debugging the camera.

Note that where we're logging times, we're logging them as these strange numbers. These are [Unix timestamps](https://en.wikipedia.org/wiki/Unix_time), and describe the number of seconds since the Unix epoch.

### Running the camera on boot

There are a number of ways to make the camera start when the Pi does. We're going to use [supervisor](http://supervisord.org/), a Python based process monitoring tool.

* Install supervisor: `sudo apt-get install supervisor`
* Configure supervisor: `sudo nano -w /etc/supervisor/conf.d/catflap.conf`

The last command will again open `nano`, and we can write the following simple configuration file:

    [program:catflap]
    command=/opt/catflap-camera/camera.py

That's all we need - this tells supervisor how to run the camera, and it'll look after starting it at boot and restarting it if it falls over. Again recall we need to enter `Ctrl+O` to write the file and `Ctrl+X` to close `nano`.

## Testing

Once you've got the Pi in place and the sensor and magnet attached to the catflap, plug it all in and turn it on. You should be able to see your Pi on the network and view the web server to see the pictures from your camera. Pushing the catflap should take a picture. Wait 2 seconds and push it again and you should get another picture. 

You're set! Now go and lurk somewhere and wait for your cat to go through the flap. Once it has, you can see the result on your Pi's web server.

## Next steps

Now you're collecting pictures of your catflap, you can do all sorts of fun things with the data - seeing when your cat is leaving the house, spotting intruders, and so on! For instance, these graphs were produced using the [nvd3](http://nvd3.org/) javascript charting tool:

![Stats example](https://github.com/JamesHarrison/catflap-camera/raw/master/docs/images/catstats.png "An example of data generated from the catflap")

Some [suggestions on extending the software](../master/docs/EXTENDING.md) can be found in this git repository; there are a lot of guides out on the net for how to do things with your Raspberry Pi, and the [Raspberry Pi](http://raspberrypi.org/) site is a great starting point to find out more about physical computing. Happy hacking!
