import paho.mqtt.client as mqtt
import ssl
import json
import ibm_db
import ibm_db_dbi
import datetime

broker_url = "192.168.1.17"
broker_port = 8883

def insertDataSensor1(dataPayload):
   payload_dict = json.loads(dataPayload)
   deviceid = payload_dict["deviceuid"]
   devicename = payload_dict["devicename"]
   
   conn_str='DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=kjc46687;PWD=hmr22pd^whlqr2sp'
   
   
   ibm_db_conn = ibm_db.connect(conn_str,'','')
   conn = ibm_db_dbi.Connection(ibm_db_conn)
   cur = conn.cursor()
   
   if "lightmeter" in payload_dict:
      valueName = payload_dict["lightmeter"]
      insert = "INSERT INTO sensorData (deviceuid, devicename, name, valueName, currentTime) VALUES (?, ?, ?, ?, ?)"
      cur.execute(insert, (deviceid, devicename, "lightmeter", valueName, datetime.datetime.now()))
   elif "barometer" in payload_dict:
      valueName = str(payload_dict["barometer"][0]) + ", " + str(payload_dict["barometer"][1])      
      insert = "INSERT INTO sensorData (deviceuid, devicename, name, valueName, currentTime) VALUES (?, ?, ?, ?, ?)"
      cur.execute(insert, (deviceid, devicename, "barometer", valueName, datetime.datetime.now()))
   elif "IRtemperature" in payload_dict:
      valueName = str(payload_dict["IRtemperature"][0]) + ", " + str(payload_dict["IRtemperature"][1])
      insert = "INSERT INTO sensorData (deviceuid, devicename, name, valueName, currentTime) VALUES (?, ?, ?, ?, ?)"
      cur.execute(insert, (deviceid, devicename, "IRtemperature", valueName, datetime.datetime.now()))

   select="select * from sensorData"   
   cur.execute(select)

   row=cur.fetchall()
   print(row)
   
   cur.close()
   conn.close()
def on_connect(client, userdata, flags, rc):
   print("Connected With Result Code " (rc))

def on_message_from_sensortag(client, userdata, message):   
   print("Message Recieved from sensortag: "+message.payload.decode())
   person_dict = json.loads(message.payload.decode())
   insertDataSensor1(message.payload.decode())
   

client = mqtt.Client()
client.on_connect = on_message_from_sensortag
#To Process Every Other Message
client.on_message = on_message_from_sensortag

client.tls_set("C:\\Program Files\\mosquitto\\certs\\ca.crt", certfile="C:\\Program Files\\mosquitto\\certs\\server.crt", keyfile="C:\\Program Files\\mosquitto\\certs\\server.key",
               cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1_2)

client.connect(broker_url, broker_port)

client.subscribe("sensortag", qos=1)

client.message_callback_add("sensortag", on_message_from_sensortag)


client.loop_forever()

