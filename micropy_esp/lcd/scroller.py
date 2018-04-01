from time import sleep_ms, ticks_ms
from machine import I2C, Pin
from esp8266_i2c_lcd import I2cLcd

def scroll(long_string):
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
    lcd = I2cLcd(i2c, 0x3F, 2, 16)

    framebuffer1 = 'Message:'
    sleep_ms(2000)
    lcd.clear()
    # long_string = 'This string is too long to fit 1 1 Hello!'
    for i in range(len(long_string) - 16 + 1):
        framebuffer =(framebuffer1+'\n'+ long_string[i:i+16])
        lcd.clear()
        lcd.putstr(framebuffer)
        sleep_ms(300)
    lcd.clear()
