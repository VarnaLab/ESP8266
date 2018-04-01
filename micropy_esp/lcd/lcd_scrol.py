from time import sleep_ms, ticks_ms
from machine import I2C, Pin
from esp8266_i2c_lcd import I2cLcd

def mess(long_string):
    
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
    lcd = I2cLcd(i2c, 0x3F, 2, 16)
    lcd.putstr(" New\n Message:")
    framebuffer1 = 'Message:'
    sleep_ms(2000)
    lcd.clear()
    framebuffer =(framebuffer1+'\n'+ long_string)
    lcd.putstr(framebuffer)
    for i in range(len(long_string) - 16 + 1):
        lcd.clear()
        framebuffer =(framebuffer1+'\n'+ long_string[i:i+16])
        lcd.putstr(framebuffer)
        sleep_ms(300)
        
   