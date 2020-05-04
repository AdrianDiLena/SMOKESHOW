from umqtt.robust import MQTTClient
import dht
import machine
import utime
import ntptime
import webrepl

webrepl.start()
ntptime.settime()

builtinLED = machine.Pin(2, machine.Pin.OUT)

p12 = machine.Pin(12, machine.Pin.OUT) # relay 1 - humidifier
p13 = machine.Pin(13, machine.Pin.OUT) # relay 3 - led
p14 = machine.Pin(14, machine.Pin.OUT) # relay 2 - fan

d = dht.DHT22(machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP))

client = MQTTClient('124748937892378493027345', '192.168.2.67')
client.connect()

while True:
    d.measure() # measure temp + hum
    utime.sleep(5) # wait 5 seconds, must be at least 750 ms for DHT22 sensor
    client.publish('fruits_temp', str(d.temperature())) # publishes temp to mqtt broker
    client.publish('fruits_hum', str(d.humidity())) # publishes hum to mqtt broker
    
    # Humidifier turns on fist 9 minutes of each hour or if under 98% humidity.
    if d.humidity() < 98:
        p12.off()
    elif machine.RTC().datetime()[5] < 10:
        p12.off()
    else:
        p12.on()

    # Fan turns on for the last 3 minutes of every hour.
    if machine.RTC().datetime()[5] > 56:
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
    print('..................................')        
    print(machine.RTC().datetime()[])
    print('Humidity: ' + str(d.humidity()) + ' %')
    print('Temperature: ' + str(d.temperature()) + ' C')
    if p12.value() == 0:
        print('Humidifier   ON')
    else:
        print('Humidifier   OFF')
    if p13.value() == 0:
        print('Lights       ON')
    else:
        print('Lights       OFF')
    if p14.value() == 0:
        print('Fan          ON')
    else:
        print('Fan          OFF')
    print('..................................')        