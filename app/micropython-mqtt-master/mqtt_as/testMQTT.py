from mqtt_as import MQTTClient
from config import config
import uasyncio as asyncio

SERVER = 'eu.thethings.network'  # Change to suit e.g. 'iot.eclipse.org'
# Код изпълнен при постъпване на съобщение
def callback(topic, msg):
    print((topic, msg))
# Код изпълнен след свързване с que-то. Абонира се за съобщения
async def conn_han(client):
    await client.subscribe('testtem1', 1)

async def main(client):
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
config['user'] = 'testgandipg'
config['password'] = 'ttn-account-v2.kpUOPdCpDUSxr3kVi3ktOG71_nprs0Nxu9uHu54eiLQ'

MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
