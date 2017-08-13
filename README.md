# RaspberryPI based room air quality data collector

This project uses a [10,000ppm MH-Z16 NDIR CO2 Sensor](http://sandboxelectronics.com/?product=mh-z16-ndir-co2-sensor-with-i2cuart-5v3-3v-interface-for-arduinoraspeberry-pi) 
to measure the CO2 concentration within the room air and a DHT11/DHT22 for the temperature and humidity measurement.
The data collected is sent to a InfluxDB from which it can by visualized via a graphical UI like [Grafana](https://grafana.com/).

<img src="https://gehridav.github.io/img/co2-temp-pi-project.jpg" width="500"/>
   
## Needed software:
### DHT22
A library to access the DHT22 sensor can be found on [GitHub](https://github.com/adafruit/Adafruit_Python_DHT). Clone the 
repo to your system and build it. Before you run this, make sure your system is able to compile Python extensions. This can be done via:
```
sudo apt-get update
sudo apt-get install build-essential python-dev
```
When this is fine, the library can be downloaded and built like that:

```
git clone https://github.com/adafruit/Adafruit_Python_DHT.git && cd Adafruit_Python_DHT
sudo python setup.py install
```
If you have the DHT22 sensor connected to GPIO 24, you can test the sensor by calling an example script that comes with the library:
```
sudo ./examples/AdafruitDHT.py 22 24
```

### MH-Z16

#### I2C

The code used here is based on the source code from [Sandbox electronics](https://github.com/SandboxElectronics/NDIR). 
A [technical documentation](http://sandboxelectronics.com/?p=1126) about the sensor can be found also on their website.
As the sensor communicates with the PI via I2C, make sure that it's enabled on your PI. 
```
sudo apt-get update
sudo apt-get install libi2c-dev
```
Make sure that i2c is enabled at boot time:
```
sudo vi /boot/config.txt
```
and check that i2c is enabled:
```
dtparam=i2c_arm=on
```
and the kernel module configured:
```
sudo vi /etd/modules
```
if not there, add the following lines
```
i2c-bcm2708
i2c-dev
```

after a reboot, the i2c interface should be activated. You can test it by calling:
```
lsmod | grep i2c_
```
what should return the two loaded modules.

#### UART

If you directly connect the sensor to the UART port of the PI, you must make sure the serial interface is enabled and the console output that by default is sent to it is disabled.
This can be done via the raspi-config tool, 5 Interfaceing-Options -> P6 Serial.  

### Influx DB client
To send the collected data into a InfluxDB database, the python client must be installed.
```
sudo pip install --upgrade pip
sudo pip install --upgrade influxdb
``` 
 
## Connecting DHT11 to Pi
In my case, I use a DHT11 sensor coming together with a pull-up resistor on a small board. It has three connectors, from left to right:
 DHT11 signal (GPIO), +3.3V input, GND.

## Connecting DHT22 to Pi
As it turned out that the DHT11 sensor is quite inaccurate, I replaced it with a [DHT22 board](https://www.aliexpress.com/item/DHT22-AM2302-Digital-Temperature-And-Humidity-Sensor-Module-Replace-SHT11-SHT15/2038550076.html) that has a pull-up resistor included. There the connectors are like this (left to right): +3.3V input, DHT22 signal (GPIO), GND.
 
