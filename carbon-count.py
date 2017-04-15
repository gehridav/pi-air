# import NDIR
import time
import json
import datetime
import ConfigParser

#from influxdb import InfluxDBClient
#import Adafruit_DHT



class Measurement:

    def __init__(self, session, runNo, time, ppm, temperature, humidity):
        self.measurement = session
        self.tags  = {'run': runNo}
        self.time = time
        self.fields = {'ppm': ppm, 'temperature': temperature, 'humidity': humidity}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

# Load configuration
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

# Initialize sensors
sensor = NDIR.Sensor(Config.getint('Co2Sensor','Address'))
#sensor.begin()
#tmpSensor = Adafruit_DHT.DHT11
tmpSensorPin = Config.getint('TempSensor','Gpio')


# Initialize InfluxDb client
#client = InfluxDBClient(Config.get('InfluxDb','Host'), Config.get('InfluxDb','Port'), Config.get('InfluxDb','User'), Config.get('InfluxDb','Password'), Config.get('InfluxDb','Dbname'), True, True)


#Initialize current session
session = Config.get('InfluxDb','Session')
now = datetime.datetime.now()
runNo = Config.get('InfluxDb','RunPrefix') + now.strftime("%Y%m%d%H%M")



try:
    while True:
        # sensor.measure()
        humidity, temperature = 10, 11  # Adafruit_DHT.read_retry(tmpSensor, tmpSensorPin)

        utc_datetime = datetime.datetime.utcnow()
        iso = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")

        try:
            # client.write_points(Measurement(session, runNo, iso, 1234, temperature, humidity).toJSON())
            print("Round:")
            #measurement = Measurement(session, runNo, iso, 1234, temperature, humidity)
            print("print")
            print(Measurement(session, runNo, iso, 1234, temperature, humidity).toJSON())
        except Exception as ex:
            print ex

        time.sleep(20)
except KeyboardInterrupt:
    pass

