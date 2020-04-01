## AWS Greengrass core Lambda functions

## Overview
This document provides information for GGC Lambda functions

## Features
 * EdgeComputeLambda
 * messageRobotLambda
 * updataLambda
 * uptimeRobotLambda

### EdgeComputeLambda
This Lambda function compute the temperature data from device thing (Switch Thing), then forward the result to another device thing (RobotArm Thing) to perform the command (Power ON/OFF the KW41 Thread lamp). 
### messageRobotLambda
This Lambda function receive the message/command (for example, Lamp ON of OFF) from Cloud side, then forward this command to RobotArm Thing to power on or off the lamp.
### updataLambda
This Lambda function update the temperature data to Amazon Web server to show the run-time data ("greengrass.co4tctnwmzmy.us-west-2.rds.amazonaws.com"). Add update the temperature data to cloud side through topic "/topic/mytemp".
### uptimeRobotLambda
This Lambda function update the stat of RobotArm Thing to Cloud sidei through topic "/topic/metering".
