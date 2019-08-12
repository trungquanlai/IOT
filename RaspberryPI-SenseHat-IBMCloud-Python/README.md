# Sense Hat Sensor Signals with Watson IOT Platform and Raspberry Pi
### Author: Trung Quan Lai
In this project, The Watson IOT Platform was used as the endpoint where devices send data to and send these data to subscribe to clients by using MQTT protocol. 

Publish Client and Subscribe Client was developed by using Python programming language and ibmiotf library to pulbish sensor signals which capture on Sense Hat and receive data from broker then display the content on Sense Hat screen.
### Instruction

The prototype contains three python files:
- Publish.py : publish sensor data.
- Subscribe.py : subscribe to topics from broker
- FetchData.py : fetch data and display on Sense Hat screen

Note: On Subscribe.py file has insert database action using MySQL Server so making sure MySQL Server is running and contains database name IOTDB which contains three tables D001, D002 and D003 following format:

| id | text | value | timestamp |
