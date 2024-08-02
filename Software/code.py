import time
from math import sqrt
import board
import busio
import microcontroller

import adafruit_tca9548a
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn

import socketpool
import wifi
from adafruit_httpserver import Server, Request, Response

i2c = busio.I2C(scl=board.GP27, sda=board.GP26)
pca = adafruit_tca9548a.PCA9546A(i2c)
        
sensor_info = [
    {"room": "Kitchen", "device": "Terminal 1", "maxamps": 5},
    {"room": "Master Bed Room", "device": "Terminal 1", "maxamps": 5},
    {"room": "Dinning Room", "device": "Terminal 1", "maxamps": 5},
    {"room": "Son Bed Room", "device": "Terminal 1", "maxamps": 5},

    {"room": "Daughter Bed Room", "device": "Terminal 1", "maxamps": 5},
    {"room": "Hall", "device": "Terminal 1", "maxamps": 5},
    {"room": "Kitchen", "device": "Terminal 2", "maxamps": 15},
    {"room": "Daughter Bed Room", "device": "Geyser", "maxamps": 15},

    {"room": "Son Bed Room", "device": "AC", "maxamps": 30},
    {"room": "Daughter Bed Room", "device": "AC", "maxamps": 30},
    {"room": "Hall", "device": "AC", "maxamps": 30},
    {"room": "Kitchen", "device": "Terminal 3", "maxamps": 15},

    {"room": "Son Bed Room", "device": "Geyser", "maxamps": 15},
    {"room": "Master Bed Room", "device": "Geyser", "maxamps": 15},
    {"room": "Master Bed Room", "device": "AC", "maxamps": 30},
    {"room": "Dinning Room", "device": "AC", "maxamps": 30},
]

addresses = [0x48, 0x49]
channels = [(ADS.P2, ADS.P3), (ADS.P0, ADS.P1)]
current_sensors = []
for i in reversed(range(4)):
    for address in addresses:
        for channel in channels:
            current_sensors.append({"pca_channel": i, "ads_address": address, "ads_channel": channel})

SAMPLE_DURATION = 80
RATE = 860

def setup_sensor_objects():
    for channel in range(4):
        for address in addresses:
            ads = ADS.ADS1115(pca[channel], address=address, gain=4)
            ads.data_rate = RATE
            ads.mode = Mode.CONTINUOUS

            for sensor in current_sensors:
                if sensor['pca_channel'] == channel and sensor['ads_address'] == address:
                    ads_channel = sensor["ads_channel"]
                    sensor["ads_channel_object"] = AnalogIn(ads, ads_channel[0], ads_channel[1])
                    _ = sensor["ads_channel_object"].value

def update_voltage_reading():
    samples = int(SAMPLE_DURATION * RATE / 1000) + 1
    for sensor in current_sensors:
        sensor['data'] = 0

    for i in range(samples):
        for sensor in current_sensors:
            if sensor["ads_channel"] == (ADS.P0, ADS.P1):
                sct_device = sensor["ads_channel_object"]
                sensor['data'] += sct_device.voltage ** 2

    for i in range(samples):
        for sensor in current_sensors:
            if sensor["ads_channel"] == (ADS.P2, ADS.P3):
                sct_device = sensor["ads_channel_object"]
                sensor['data'] += sct_device.voltage ** 2

    for sensor in current_sensors:
        sensor['data'] = sqrt( sensor['data'] / samples )

def get_data():
    html = '# PowerTiger - Home Energy Consumption Metrics\n'
    html += 'cpu_temperature{{device="CPU"}} {}\n'.format(microcontroller.cpu.temperature)
    update_voltage_reading()
    for idx, sensor in enumerate(current_sensors):
        s_info = sensor_info[idx]
        sct_sensor = sensor["ads_channel_object"]
        vname = (s_info["room"] + " " + s_info["device"]).replace(" ", "_").lower()
        amps = int(sensor['data'] * s_info["maxamps"] * 1000)
        html += '{}{{room="{}",device="{}"}} {}\n'.format(vname, s_info["room"], s_info["device"], amps)

    return html

setup_sensor_objects()

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/metrics", debug=True)

@server.route("/metrics", append_slash=True)
def metrics_handler(request: Request):
    return Response(request, body=get_data(), content_type="text/plain")

server.serve_forever(str(wifi.radio.ipv4_address))