import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

ssid = 'VIRGIN930'
password = '6AF7AD59'
mqtt_server = '192.168.2.67'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = 124312341234
topic_sub = b'fruits_fan'

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Welcome to the $MoKe$HOW')
print(station.ifconfig())