#imports of necessary libraries and modules
#Hardware
from machine import Pin, I2C
import bme280
#Data Handling
import time
 
#Initialization of the I2C protocol
i2c=I2C(0, sda=Pin(0), scl=Pin(1), freq= 40000)
 
#instance of the bme280 with I2C initialized
bme = bme280.BME280(i2c=i2c)
#create a for loop 8 times to read the data 
for i in range(8):
    
    #Reading data from sensors and storing the values on the variables temp, pressure and humidity. 
    temp = bme.values[0]
    pressure = bme.values[1]
    humidity = bme.values[2]
    
    #concatenation of variables and strings to form a readable string
    reading = 'Current Temperature: |' + temp + '| Current Humidity: ' + humidity + '| Cureent Pressure: ' + pressure
    
    #print the string with values
    print(reading)
    #pause the loop for 1 second
    time.sleep_ms(1000)