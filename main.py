from umqtt.robust import MQTTClient
import dht
import machine
import utime
import webrepl
import ntptime

ntptime.settime()

webrepl.start()

client_id = '12345'
mqtt_server = '192.168.2.67'
topic_sub = b'SMOKESHOW/relays/#'

print('\n\nWelcome to Operation SMOKESHOW\nVersion Delta - 6/8/2020\nThreat Level: Midnight\n')

client = MQTTClient(client_id, mqtt_server)
client.connect()

d = dht.DHT22(machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP))

led = machine.Pin(2, machine.Pin.OUT)

p12 = machine.Pin(12, machine.Pin.OUT) # relay 1 - fan
p5 = machine.Pin(5, machine.Pin.OUT) # relay - 4 humidifier fan
p13 = machine.Pin(13, machine.Pin.OUT) # relay 3 - led
p14 = machine.Pin(14, machine.Pin.OUT) # relay 2 - humidifier

pins = [p12, p5, p13, p14, led]
for i in pins[:]:
    i.on()

def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'SMOKESHOW/relays/light' and msg == b'on':
        p13.off()      
    elif topic == b'SMOKESHOW/relays/light' and msg == b'off':
        p13.on()
    if topic == b'SMOKESHOW/relays/fan' and msg == b'on':
        p12.off()
    elif topic == b'SMOKESHOW/relays/fan' and msg == b'off':
        p12.on()
    if topic == b'SMOKESHOW/relays/humidifier' and msg == b'on':
        p14.off()
        p5.off()
    elif topic == b'SMOKESHOW/relays/humidifier' and msg == b'off':
        p14.on()
        p5.on()


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
    led.off()
    utime.sleep_ms(50)
    led.on()
    utime.sleep_ms(950) # wait 2 seconds, must be at least 750 ms for DHT22 sensor
    d.measure() # measure temp + hum
    client.publish('fruits_temp', str(d.temperature())) # publishes temp to mqtt broker
    client.publish('fruits_hum', str(d.humidity())) # publishes hum to mqtt broker
    
    # Humidifier turns on fist 4 minutes of each hour or if under 98% humidity.
    if d.humidity() < 98:
        p14.off()
        p5.off()
    elif utime.localtime()[4] < 2:
        p14.off()
        p5.off()
    elif topic == b'SMOKESHOW/relays/humidifier' and msg == b'on':
        p14.off()
        p5.off()
    else:
        p14.on()
        p5.on()
    # Fan turns on for the last 2 minutes of every hour.
    if utime.localtime()[4] > 57: 
        p12.off()
    elif topic == b'SMOKESHOW/relays/fan' and msg == b'on':
        p12.off()
    else:
        p12.on()
    # LED turns on for the first 5 minutes of every hour.
    if utime.localtime()[4] < 5: 
        p13.off()
    elif topic == b'SMOKESHOW/relays/light' and msg == b'on':
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
        print('Fan               ON')
    else:
        print('Fan               OFF')
    if p13.value() == 0:
        print('Lights            ON')
    else:
        print('Lights            OFF')
    if p14.value() == 0:
        print('Humidifier        ON')
    else:
        print('Humidifier        OFF')
    if p5.value() == 0:
        print('Humidifier Fan    ON')
    else:
        print('Humidifier Fan    OFF')
    print('..................................')

    try:
        client.check_msg()
    except OSError as e:
        restart_and_reconnect()