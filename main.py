from umqtt.robust import MQTTClient
import dht
import machine
import utime
import ntptime

ntptime.settime()

builtinLED = machine.Pin(2, machine.Pin.OUT)
p12 = machine.Pin(12, machine.Pin.OUT) # relay 1 - humidifier
p13 = machine.Pin(13, machine.Pin.OUT) # relay 3 - led
p14 = machine.Pin(14, machine.Pin.OUT) # relay 2 - fan
d = dht.DHT22(machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP))

client = MQTTClient('124748937892378493027345', '192.168.2.67')
client.connect()

while True:
    d.measure()
    utime.sleep(3)
    client.publish('fruits_temp', str(d.temperature()))
    client.publish('fruits_hum', str(d.humidity()))


    if d.humidity() < 98:
        p12.off()
    elif d.humidity() > 98:
        p12.on()
    elif machine.RTC().datetime()[5] < 10:
        p12.off()

    print(machine.RTC().datetime())

    if machine.RTC().datetime()[5] > 57:
        p14.off()
    else:
        p14.on()
    if machine.RTC().datetime()[4] > 13:
        p13.off()
    else:
        p13.on()
    if machine.RTC().datetime()[5] < 10:
        p12.off()
        