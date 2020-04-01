#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

import sys
import logging
import json
import greengrasssdk
import os
import string


# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

client = greengrasssdk.client('iot-data')

target_offset = '30'
target_temp = '300'

def message_handler(event, context):
	global target_temp
	global target_offset
	logger.info("Received message! %s", event)
	if 'target' in event or 'offset' in event:
		if 'target' in event and event['target'] < '500' and event['target'] > '200':
			target_temp = event['target']
		if 'offset' in event and event['offset'] != '0':
			target_offset = event['offset']
		payload_t = '{"state":{"desired":{"myState":"' + target_temp + ':' + target_offset + '"}}}'
		client.update_thing_shadow(thingName = "aws-actuator-thing", payload = payload_t)
		logger.info("Triggering publish to shadow topic to set target temperature")

	if 'state' in event and 'desired' in event['state'] and 'mytemp' in event['state']['desired']:
		temp = event['state']['desired']['mytemp']
		if int(temp) > (int(target_temp) + int(target_offset)):
			client.update_thing_shadow(thingName = "aws-actuator-thing", payload = '{"state":{"desired":{"myState":"red"}}}')
			logger.info("Triggering publish to shadow topic to set light to red, and start fan")
		elif int(temp) < (int(target_temp) - int(target_offset)):
			client.update_thing_shadow(thingName = "aws-actuator-thing", payload = '{"state":{"desired":{"myState":"blue"}}}')
			logger.info("Triggering publish to shadow topic to set light to blue, and start heater")
		else:
			client.update_thing_shadow(thingName = "aws-actuator-thing", payload = '{"state":{"desired":{"myState":"green"}}}')
			logger.info("Triggering publish to shadow topic to set light green")
