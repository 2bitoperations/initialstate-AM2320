import board
import busio
import adafruit_am2320
import logging
import json
import time
import sys
from ISStreamer.Streamer import Streamer

rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
rootLogger.addHandler(ch)

fileLogger = logging.FileHandler("/tmp/server.log")
fileLogger.setLevel(logging.WARN)
fileLogger.setFormatter(formatter)
rootLogger.addHandler(fileLogger)

with open('config.json') as f:
    config = json.load(f)

BUCKET_NAME = config['bucket_name']
BUCKET_KEY = config['bucket_key']
ACCESS_KEY = config['access_key']

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_am2320.AM2320(i2c)

streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

while True:
    try:
        rh = sensor.relative_humidity
        temp = sensor.temperature
        logging.info("logging temp as {temp} rh as {rh}".format(temp=temp, rh=rh))
        streamer.log('bucket_rh', rh)
        streamer.log('bucket_temp', temp)
    except:
        logging.exception("everything broke")

    time.sleep(60)