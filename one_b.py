#imports of necessary libraries and modules
from machine import Pin, I2C
import bme280
from time import sleep
#Networking 
import network
import socket

#Initialization of the I2C protocol 
i2c=I2C(0, sda=Pin(0), scl=Pin(1), freq= 40000)
#instance of the bme280 with I2C initialized 
bme = bme280.BME280(i2c=i2c)


#Hotspot credentials 
ssid = 'iPhoneH'
password = 'qwerty123'

#function to connect to WLAN
def connect(): 
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

#function to open a socket
def open_socket(ip):
    
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

#create html template
def webpage(reading):
    
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>Pico W Temperature</title>
            <meta http-equiv='refresh' content='10'>
            <style>
                h1 {{
                    text-align: center;
                }}
            </style>
            </head>
            <body>
            
            <h1>Readers</h1>
            <p>{reading}</p>
            
            </body>
            </html>
            """
    return str(html)

#function to send sensor data to a webpage
def serve(connection):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        #Reading data from sensors and storing the values on the variables temp, pressure and humidity       
        temp = bme.values[0]
        pressure = bme.values[1]
        humidity = bme.values[2]
    
        reading = f'Current Temperature: {temp} | Current Humidity: {humidity} | Current Pressure: {pressure}'
        
        html = webpage(reading)
        client.send(html)

client.close()

#Implements try-except mechanism to connect to the network, open socket for data serving, and handle KeyboardInterrupt with device reset
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
