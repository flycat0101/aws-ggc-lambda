#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

import sys
import logging
import json
import greengrasssdk
import os
import string
import insertdata.addsql as sdata


# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

client = greengrasssdk.client('iot-data')
insertData = sdata.InsertData()

def message_handler(event, context):
	logger.info("Received message! %s", event)
	if 'state' in event and 'desired' in event['state'] and 'mytemp' in event['state']['desired']:
		temp = event['state']['desired']['mytemp']
		stemp = str(temp)
		datet = event['state']['desired']['datetime']
		temp_dt = stemp + "," + "\"" + datet + "\""
		insertData.check_data(temp_dt)
		client.publish(topic = '/topic/mytemp', payload = temp_dt)
