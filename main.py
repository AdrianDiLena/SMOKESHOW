from umqtt.robust import MQTTClient
import dht
import machine
import utime
import ntptime
import webrepl

webrepl.start()
ntptime.settime()

builtinLED = machine.Pin(2, machine.Pin.OUT)
builtinLED.on()

p12 = machine.Pin(12, machine.Pin.OUT) # relay 1 - humidifier
p5 = machine.Pin(5, machine.Pin.OUT) # relay - 4 humidifier fan
p13 = machine.Pin(13, machine.Pin.OUT) # relay 3 - led
p14 = machine.Pin(14, machine.Pin.OUT) # relay 2 - fan

pins = [p12, p5, p13, p14]
for i in pins[:]:
    i.on()

d = dht.DHT22(machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP))

client = MQTTClient('124748937892378493027345', '192.168.2.67')
client.connect()

def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'SMOKESHOW/relays/light' and msg == b'on':
        p13.off()      
    elif topic == b'SMOKESHOW/relays/light' and msg == b'off':
        p13.on()
    if topic == b'SMOKESHOW/relays/fan' and msg == b'on':
        p14.off()
    elif topic == b'SMOKESHOW/relays/fan' and msg == b'off':
        p14.on()


def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to: %s \nSubscribed to: %s' % (mqtt_server, topic_sub))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
    utime.sleep(2) # wait 5 seconds, must be at least 750 ms for DHT22 sensor
    d.measure() # measure temp + hum
    client.publish('fruits_temp', str(d.temperature())) # publishes temp to mqtt broker
    client.publish('fruits_hum', str(d.humidity())) # publishes hum to mqtt broker
    
    # Humidifier turns on fist 9 minutes of each hour or if under 98% humidity.
    if d.humidity() < 98:
        p12.off()
        p5.off()
    elif machine.RTC().datetime()[5] < 4:
        p12.off()
        p5.off()
    else:
        p12.on()
        p5.on()

    # Fan turns on for the last 3 minutes of every hour.
    if machine.RTC().datetime()[5] > 57:
        p14.off()
    else:
        p14.on()
    
    # LED turns on for the first 4 minutes of every hour.
    if machine.RTC().datetime()[5] < 5: 
        p13.off()
    else:
        p13.on()
    
    # Terminal prints & debugging
    print('Operation SmokeShow')
    print('----------------------------------')        
    print(machine.RTC().datetime())
    print('Humidity:         ' + str(d.humidity()) + ' %')
    print('Temperature:      ' + str(d.temperature()) + ' C')

    if p12.value() == 0:
        print('Humidifier        ON')
        client.publish('SMOKESHOW/machines/humidifer', 'ON') # publishes hum to mqtt broker
    else:
        print('Humidifier        OFF')
        client.publish('SMOKESHOW/machines/humidifer', 'OFF')
    if p13.value() == 0:
        print('Lights            ON')
        client.publish('SMOKESHOW/machines/light', 'ON')
    else:
        print('Lights            OFF')
        client.publish('SMOKESHOW/machines/light', 'OFF')
    if p14.value() == 0:
        print('Fan               ON')
        client.publish('SMOKESHOW/machines/fan', 'ON')
    else:
        print('Fan               OFF')
        client.publish('SMOKESHOW/machines/light', 'OFF')
    if p5.value() == 0:
        print('Humidifier Fan    ON')
        client.publish('SMOKESHOW/machines/hfan', 'ON')
    else:
        print('Humidifier Fan    OFF')
        client.publish('SMOKESHOW/machines/hlight', 'OFF')
    print('..................................')        