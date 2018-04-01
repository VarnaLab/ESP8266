# This file is executed on every boot (including wake-boot from deepsleep)
import esp
 esp.osdebug(None)

# init logging
import logging
logSocket = open('log.txt','a') 
logging.basicConfig(stream=logSocket)
logger = logging.getLogger('Boot')

logger.info('Starting new session. Connecting to wifi...')
try:
    import gc
    from autoconnect import connect
    connected = connect()
    gc.collect()
    if connected:    
        logger.info('Starting webrepl.')
        import webrepl

        webrepl.start()
        gc.collect()
        logger.info("Webrepl started successfully")
    else:
        logger.info('FAILED TO CONNECT! Connect manually and start webrepl from start')
        logSocket.close()
except Exception as e:
    logger.error("Error occured while booting:{}".format(e))
    logSocket.close()
    
logSocket.close()