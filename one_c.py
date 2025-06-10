#imports of necessary libraries and modules
#Hardware 
import machine
from machine import Pin, I2C
import bme280
#Networking 
import network
import urequests
#Data Handling
import time
import json
import gc

#Setting up wlan for the hotspot and initialize the LED as output device
wlan = network.WLAN(network.STA_IF)
board_led = machine.Pin("LED", machine.Pin.OUT)

#Initialization of the I2C protocol 
i2c=I2C(0, sda=Pin(0), scl=Pin(1), freq= 40000)
#instance of the bme280 with I2C initialized 
bme = bme280.BME280(i2c=i2c)

#Hotspot credentials
Wifi_ssid = 'iPhoneH'
Wifi_password = 'qwerty123'

#URLs for Google Script to log data and API for current time
SHE_URL = "https://script.google.com/macros/s/AKfycbywS64ieptzcryzjx6wB7QxyD9Jz439sbxb_UaGtCbAabqLm9VeHHUTBnkaXdGXiElD/exec"
TIME_URL = "https://timeapi.io/api/Time/current/zone?timeZone=Europe/London"

#function to get current time using http
def getCurrentTime():
    res = urequests.get(url=TIME_URL)
    time_data = json.loads(res.text)["dateTime"]
    res.close()
    return time_data

#function to connect to the hotspot
def connectWiFi():
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected() and wlan.status() >= 0:
            print("Waiting to connect: ")
            time.sleep(1)
            board_led.value(not board_led.value())  # Toggle LED
        board_led.on()
        print(wlan.ifconfig())
    else:
        print("Wifi already connected...")
        #print current time 
        print(getCurrentTime())

#function to send sensor data to the spreadsheet using the url in line 28
def sendToSpreadsheet(time, temp, pressure, humidity):
    try:
        url = f"{SCRIPT_URL}?time={time}&temp={temp}&pressure={pressure}&humidity={humidity}"
        print(url)
        res = urequests.get(url=url)
        res.close()
        gc.collect()
    except Exception as e:
        print("Error...", e)

#Connect to hotspot
connectWiFi()

#create a for loop 10 times to read the data from the sensor and sent it to the spreadsheet
for i in range(10):
    
    value = bme.read_compensated_data()
    
    #Reading data from sensors, storing the values on the variables and divide for meaningful units
    temp = value[0] / 100.0  
    pressure = value[1] / 25600.0  
    humidity = value[2] / 1024.0
    
    #get current time 
    timestamp = getCurrentTime()
    
    #send the data to the spreadsheet
    sendToSpreadsheet(time=timestamp, temp=temp, pressure=pressure, humidity=humidity)
    #interval of 5 second between one reading and the next one
    time.sleep(5)

#tunr off the LED light after the readings
board_led.off()

