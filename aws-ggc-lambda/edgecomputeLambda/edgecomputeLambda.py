#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

import sys
import logging
import json
import greengrasssdk
import os
import string
import powerswitch.switch as pswitch


# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

client = greengrasssdk.client('iot-data')
powerController = pswitch.PowerSwitchController()

def message_handler(event, context):
	logger.info("Received message! %s", event)
	if 'state' in event and 'desired' in event['state'] and 'mytemp' in event['state']['desired']:
		temp = event['state']['desired']['mytemp']

		if temp > 300:
			logger.info("Triggering publish to shadow topic to set light ON")
			client.update_thing_shadow(thingName = "RobotArm_Thing", payload = '{"state":{"desired":{"myState":"on"}}}')
			#powerController.switch('on')
		else:
			logger.info("Triggering publish to shadow topic to set light OFF")
			client.update_thing_shadow(thingName = "RobotArm_Thing", payload = '{"state":{"desired":{"myState":"off"}}}')
			#powerController.switch('off')
	
