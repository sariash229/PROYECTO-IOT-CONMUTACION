import anvil.pico
import uasyncio as a
from machine import Pin, I2C
from time import sleep
import dht
from pico_i2c_lcd import I2cLcd

# This is an example Anvil Uplink script for the Pico W.
# See https://anvil.works/pico for more information

UPLINK_KEY = "Tu clave de anvil"

# We use the LED to indicate server calls and responses.
led = Pin("LED", Pin.OUT, value=1)
sensor = dht.DHT11(Pin(2)) 
i2c = I2C(0, sda=Pin (0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
lcd.backlight_on()
lcd.blink_cursor_on()
# Call this function from your Anvil app:
#
#    anvil.server.call('pico_fn', 42)
#

@anvil.pico.callable(is_async=True)
async def pico_fn(n):
    # Output will go to the Pico W serial port
    print(f"Called local function with argument: {n}")

    # Blink the LED and then double the argument and return it.
    led.toggle()
@anvil.pico.callable(is_async=True)
async def dht11data():
    sensor.measure()
    temp = round(sensor.temperature(),1)
    hum = round(sensor.humidity(),1)
    data = ("Теmperatura: {}°C Humedad: {:.0f}% ".format(temp, hum))
    print(data)
    return (data)

@anvil.pico.callable(is_async=True)
async def show_message(message):
    for i in range(3): 
        lcd .backlight_on() 
        sleep(0.2) 
        lcd.backlight_off() 
        sleep(0.2)
    lcd.backlight_on( )
    lcd.putstr(message)
    sleep(10) 
    lcd.clear ()
    
@anvil.pico.callable(is_async=True)
async def show_message1():
    sensor.measure()
    hum = round(sensor.humidity(),1)
    if hum <=50 :
        for i in range(3): 
            lcd .backlight_on() 
            sleep(0.2) 
            lcd.backlight_off() 
            sleep(0.2)
        lcd.backlight_on( )
        lcd.putstr("Estamos bien")
        sleep(10) 
        lcd.clear ()
    else:
        for i in range(3): 
            lcd .backlight_on() 
            sleep(0.2) 
            lcd.backlight_off() 
            sleep(0.2)
        lcd.backlight_on( )
        lcd.putstr("Está humedo")
        sleep(10) 
        lcd.clear ()
# Connect the Anvil Uplink. In MicroPython, this call will block forever.

anvil.pico.connect(UPLINK_KEY)


# There's lots more you can do with Anvil on your Pico W.
#
# See https://anvil.works/pico for more information


