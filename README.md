# smoke_show

Operation Smoke Show

This is a simple code automating mycology projects. 
Using NodeMCU ESP8266 and Micropython 

- dht22 sensor is used to measure temperature and relative humidity
- humidifier is programmed to turn on if relative humidity falls below a certain threshold
- no heater is included in this version as it is unecessary in my climate, but one could be easily added. 
- 12V 5050 smd led strip light is on 12 hour on/off cycle
- 12V computer fan is programmed to turn on for one minute per hour to provide fresh oxygen.
- Sends humidity + temp data to MQTT server on Raspberry

To do List: 

- Add in OTA updates via GitHub (this should be the rule for all projects going forward)
- Increase humidifier time, perhaps setting it to a certain number of minutes per hour like the LED lights, 
  while maintaining the sensor threshold value of x % humidity. 
- co2 sensor would be interesting and allow better fine tuning of the system
- soil moisture for substrate beds? 
- Peltier element for cooling? This might be overkill but an interesting experiment.
- camera for time lapse? This might be overkill but an interesting experiment.
