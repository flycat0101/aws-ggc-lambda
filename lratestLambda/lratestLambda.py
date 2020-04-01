#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

import sys
import greengrasssdk
import os
import logging

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

client = greengrasssdk.client('iot-data')
volumepath = '/dest/LRAtest'

def message_handler(event, context):
	client.publish(topic = '/lra/test', payload = 'Sent from AWS Greengrass Core.')
	try:
		volumeinfo = os.stat(volumepath)
		client.publish(topic = '/lra/test', payload = str(volumeinfo))
		with open(volumepath + '/test', 'a') as output:
			output.write('Successfully write to a file.\n')
		with open(volumepath + '/test', 'r') as myfile:
			data = myfile.read()
		client.publish(topic = '/lra/test', payload = data)
		logger.info("Successfully write and read data, publish to cloud")
	except Exception as e:
		logger.info("Experiencing error :{}".format(e))
	return
