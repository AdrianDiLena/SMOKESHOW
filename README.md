# smoke_show

Operation Smoke Show

This is a simple code for automating terrarium projects. 
Using NodeMCU ESP8266 and Micropython 

- dht22 sensor is used to measure temperature and relative humidity
- humidifier is programmed to turn on if relative humidity falls below a certain threshold
- no heater is included in this version as it is unecessary in my climate, but one could be easily added. 
- 12V 5050 smd led strip light is on 12 hour on/off cycle
- 2x computer fan pull air out from bottom of chamber, 1 x pushes air in.
- Sends humidity + temp data to MQTT server on Raspberry Pi running Node-Red
- 1x 12v fan draws atomized mist from mason jar of water (very effective so far) 

To do List: 

- add another fan to draw air out as well. -- DONE 
- co2 sensor would be interesting and allow better fine tuning of the system.
- soil moisture for substrate beds? 
- Peltier element for cooling? This might be overkill but an interesting experiment.
- camera for time lapse? This might be overkill but an interesting experiment.
