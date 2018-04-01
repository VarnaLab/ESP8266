#!/usr/bin/env python
# -*- coding: utf-8 -*- print('import uasyncio as asyncio')
try:
    import asyncio_priority as asyncio
except ImportError:
    import uasyncio as asyncio
    
print('from config import config')
from config import config
print('from mqtt_as import MQTTClient')
from mqtt_as import MQTTClient

SERVER = 'm14.cloudmqtt.com'  # Change to suit e.g. 'iot.eclipse.org'
# Код изпълнен при постъпване на съобщение
def callback(topic, msg):
    print('Message recieved: '+(topic, msg))
# Код изпълнен след свързване с que-то. Абонира се за съобщения
async def conn_han(client):
    print('handling connection')
    await client.subscribe('testtem1', 1)

async def main(client):
    print('connecting')
    await client.connect()
    n = 0
    while True:
        await asyncio.sleep(5)
        print('publish', n)
        # If WiFi is down the following will pause for the duration.
        await client.publish('result', '{}'.format(n), qos = 1)
        n += 1

# наблъсква конфигурацията за клиента.
config['subs_cb'] = callback
config['connect_coro'] = conn_han
config['server'] = SERVER
config['port'] = '1883'
config['user'] = 'lwqlncdn'
config['password'] = 'Y1hCcwNoFEDm'

MQTTClient.DEBUG = True  # Optional: print diagnostic messages
print('creating client')
client = MQTTClient(config)
loop = asyncio.get_event_loop()
try:
    print('starting client')
    loop.run_until_complete(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors

