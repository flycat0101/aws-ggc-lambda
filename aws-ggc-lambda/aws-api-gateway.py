
import sys
# import logging
import json
import boto3

# logger = logging.getLogger(__name__)
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

client = boto3.client('iot-data')

def message_handler(event, context):
# logger.info("Received message!")
    if 'state' in event:
        if event['state'] == 'on':
            client.publish(topic = '/topic/update', qos = 1, payload = '{"state":"on"}'.encode())
            # logger.info("send message to set state to ON")
            return {'state' : 'on'}
        elif event['state'] == 'off':
            client.publish(topic = '/topic/update', qos = 1, payload = '{"state":"off"}'.encode())
            # logger.info("send message to set state to OFF")
            return {'state' : 'off'}
    elif 'offset' in event or 'target' in event:
        target_temp = '0'
        offset_temp = '0'
        if 'target' in event:
            target_temp = event['target']
        if 'offset' in event:
            offset_temp = event['offset']
        payload_t = {"target":target_temp,"offset":offset_temp}
        client.publish(topic = '/topic/target', qos = 1, payload = json.dumps(payload_t))
        return {'target' : '{}'.format(target_temp),'offset' : '{}'.format(offset_temp)}

    return {'error' : 'wrong message'}

