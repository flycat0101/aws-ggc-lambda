#
# Copyright 2010-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

# greengrassObjectClassification.py
# Demonstrates inference at edge using MXNET or TensorFlow, and Greengrass 
# core sdk. This function will continuously retrieve the predictions from the 
# ML framework and send them to the topic 'hello/world'.
#
# The function will sleep for three seconds, then repeat.  Since the function is
# long-lived it will run forever when deployed to a Greengrass core.  The handler
# will NOT be invoked in our example since we are executing an infinite loop.

import sys
import time
import greengrasssdk
import platform
import os
import argparse
import os.path
import re
from threading import Timer

import numpy as np
from six.moves import urllib
import tensorflow as tf

from importlib import import_module
from flask import Flask, render_template, Response
import argparse
import websocket
from camera_opencv import *

client = greengrasssdk.client('iot-data')
HTTP_PORT = 5000
camera_dev = 'usb'

socket_port = 9000
serverip = 'fsl.eatuo.com'

print("Initialzing face recognition engine.")
print("Using onboard usb camera")
files = os.listdir('/dev')
video_source = []
for f in files:
	if f.find('video') == 0:
		video_source.append(int(f[5:]))
if len(video_source) == 0:
	print "No usb camera found"
        exit(0)

print video_source
Camera.set_video_source(video_source)

def alter(old_file, new_file, old_strs, new_strs):
	with open(old_file, "r") as f1,open(new_file, "w") as f2:
		for line in f1:
			for i,old_str in enumerate(old_strs):
				line = re.sub(old_strs[i],new_strs[i],line)
			f2.write(line)
	f1.close()
	f2.close()

websocket.VIDEO_DEVICE = camera_dev
"""
websocket.WEBSOCKET_PORT = 9000
if serverip is None:
	alter("templates/index_static.html", "templates/index_web.html", ["WEBSOCKET_PORT"], [str(websocket.WEBSOCKET_PORT)])
else:
	alter("templates/index_static.html", "templates/index_web.html", ["WEBSOCKET_PORT","LS1046ARDB"], [str(websocket.WEBSOCKET_PORT), serverip])
"""

fdir = os.path.dirname(os.path.realpath(__file__))
tls_crt = os.path.join(fdir, 'tls', 'server.crt')
tls_key = os.path.join(fdir, 'tls', 'server.key')

app = Flask(__name__)

@app.route('/')
def index():
	"""Video streaming home page."""
	#return render_template('index_opencv.html')
	return render_template('index_web.html')

def gen(camera):
	"""Video streaming generator function."""
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
		       b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

@app.route('/videoel')
def video_feed():
	"""Video streaming route. Put this in the src attribute of an img tag."""
	if camera_dev == 'laptop':
		return Response()
	else:
		print("video_feed")
		return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/.well-known/pki-validation/fileauth.txt')
def txt_index():
	return render_template('fileauth.txt')

# Execute the function above
websocket.startWebSocketServer(serverip)
app.run(host='0.0.0.0', port=HTTP_PORT, threaded=True, ssl_context=(tls_crt, tls_key))

def function_handler(event, context):
	return
