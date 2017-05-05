import NDIR
import time
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


def validate(refValue, newValue):
        if refValue != 0:
            if newValue < refValue * 2:
                return newValue
            else:
                return refValue
        else:
            return newValue

# Load configuration
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

# Initialize sensors
sensor = NDIR.Sensor(int(Config.get('Co2Sensor','Address'),16))
sensor.begin()
tmpSensor = Adafruit_DHT.DHT22
tmpSensorPin = Config.getint('TempSensor','Gpio')

# Initialize InfluxDb client
client = InfluxDBClient(Config.get('InfluxDb','Host'), Config.get('InfluxDb','Port'), Config.get('InfluxDb','User'), Config.get('InfluxDb','Password'), Config.get('InfluxDb','Dbname'), True, True)

# Initialize current session
session = Config.get('InfluxDb','Session')
now = datetime.datetime.now()
runNo = Config.get('InfluxDb','RunPrefix') + now.strftime("%Y%m%d%H%M")

humRef = 0;
tempRef = 0;

try:
    while True:
        sensor.measure()
        hum, temp = Adafruit_DHT.read_retry(tmpSensor, tmpSensorPin)
        humRef = validate(humRef,hum)
        tempRef = validate(tempRef, temp)

        utc_datetime = datetime.datetime.utcnow()
        iso = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")

        try:
            measurement = Measurement(session, runNo, iso, sensor.ppm, tempRef, humRef)
            client.write_points([vars(measurement)])
        except Exception as ex:
            print ex

        time.sleep(Config.getint('Global','MeasureInterval'))
except KeyboardInterrupt:
    pass


