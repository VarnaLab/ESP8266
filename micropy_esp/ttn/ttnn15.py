import time
from simple import MQTTClient
import ubinascii
import json
import lcd_scrol


server='eu.thethings.network'
port=1883
user='testgandipg'
password='ttn-account-v2.kpUOPdCpDUSxr3kVi3ktOG71_nprs0Nxu9uHu54eiLQ'
btopic='testgandipg/devices/testtem1/up'

# Publish test messages e.g. with:
# mosquitto_pub -t foo_topic -m hello ///example_sub4.main('192.168.1.1',1883,'test','test1234') 

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    print((topic, msg))
    print((msg))
    j=msg
    m=j.decode()
    o = json.loads(m)
    t=(o['payload_raw'])
    print (t)
    ts=(str(ubinascii.a2b_base64(t).decode()))
    
    print (ts)
    lcd_scrol.mess(ts) 

def formatMessage(string):
    return string.lstrip("b'").rstrip("'")

def main(start='start'):
    c = MQTTClient("umqtt_client", server, port, user, password)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(btopic)
    while True:
        if True:
            # Blocking wait for message
            c.wait_msg()
        else:
            # Non-blocking wait for message
            c.check_msg()
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            time.sleep(1)

    c.disconnect()

if __name__ == "__main__":
    main()

