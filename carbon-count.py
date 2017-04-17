import NDIR
import time
import json
import datetime
import ConfigParser

from influxdb import InfluxDBClient
import Adafruit_DHT



class Measurement:

    def __init__(self, session, runNo, time, ppm, temp, hum):
        self.measurement = session
        self.tags  = {'run': runNo}
        self.time = time
        self.fields = {'ppm': ppm, 'temp': temp, 'hum': hum}

# Load configuration
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

# Initialize sensors
sensor = NDIR.Sensor(int(Config.get('Co2Sensor','Address'),16))
sensor.begin()
tmpSensor = Adafruit_DHT.DHT11
tmpSensorPin = Config.getint('TempSensor','Gpio')

# Initialize InfluxDb client
client = InfluxDBClient(Config.get('InfluxDb','Host'), Config.get('InfluxDb','Port'), Config.get('InfluxDb','User'), Config.get('InfluxDb','Password'), Config.get('InfluxDb','Dbname'), True, True)

#Initialize current session
session = Config.get('InfluxDb','Session')
now = datetime.datetime.now()
runNo = Config.get('InfluxDb','RunPrefix') + now.strftime("%Y%m%d%H%M")


try:
    while True:
        sensor.measure()
        hum, temp = Adafruit_DHT.read_retry(tmpSensor, tmpSensorPin)

        utc_datetime = datetime.datetime.utcnow()
        iso = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")

        try:
            measurement = Measurement(session, runNo, iso, sensor.ppm, temp, hum) 
            client.write_points([vars(measurement)])
            print("Round:")
            print(vars(measurement))
        except Exception as ex:
            print ex

        time.sleep(Config.getint('Global','MeasureInterval'))
except KeyboardInterrupt:
    pass

