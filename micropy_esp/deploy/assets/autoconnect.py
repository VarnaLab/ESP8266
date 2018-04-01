networks = {"WiFisengard": "cankovi15", 
            "VarnaLab-Room2": "varnalab2"}

from logging import getLogger
logger = getLogger('Autoconnect')

def is_supported_network(network_name):
    supported = False
    for n in networks:
        supported = (n == network_name)
        if supported:
            return supported
    return supported

def connect():
    try:
        import network
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        available_networks = sta_if.scan()
        for network_data in available_networks:
            network_name = network_data[0].decode()
            logger.info('Testing network:'+network_name+" if eligible.")
            if is_supported_network(network_name):
                logger.info('recognized network:' + network_name +
                    " as supported. Connecting...")
                sta_if.active(True)
                sta_if.connect(network_name, networks[network_name])
                logger.info('Connected successfully!')
                return True
    except Exception as e:
        logger.error("Error occured while autoconnecting:{}".format(e))
        return False
