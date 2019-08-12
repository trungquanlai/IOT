import ibmiotf.application
import simplejson as json
import mysql.connector
from subprocess import call

options = {
    "org": "sr7gke",
    "id": "D002",
    "auth-method": "apikey",
    "auth-key": "a-sr7gke-peofyfalld",
    "auth-token": "0EhF(z4xL9NwlxchVh",
    "port": 8883,
    "keepalive": 60,  
  }

myClient = ibmiotf.application.Client(options)

def connect():
    mydb = mysql.connector.connect(
    host="localhost",
    user="pi",
    passwd="raspberry",
    database="IOTDB"
    )
    return mydb

def insertD001(text, value, time):
    mydb = connect()
    mycursor = mydb.cursor()
    sql = "INSERT INTO D001 (id, text, value, time) VALUES (%s, %s, %s, %s)"
    val = (None, text, value, time)
    mycursor.execute(sql, val)

    mydb.commit()
    print("Last row id", mycursor.lastrowid)
    mycursor.close()
    mydb.close()
    

def insertD002(text, value, time):
    mydb = connect()
    mycursor = mydb.cursor()
    sql = "INSERT INTO D002 (id, text, value, time) VALUES (%s, %s, %s, %s)"
    val = (None, text, value, time)
    mycursor.execute(sql, val)

    mydb.commit()
    print("Last row id", mycursor.lastrowid)
    mycursor.close()
    mydb.close()
    
def insertD003(text, value, time):
    mydb = connect()
    mycursor = mydb.cursor()
    sql = "INSERT INTO D003 (id, text, value, time) VALUES (%s, %s, %s, %s)"
    val = (None, text, value, time)
    mycursor.execute(sql, val)

    mydb.commit()
    print("Last row id", mycursor.lastrowid)
    mycursor.close()
    mydb.close()

def myEventCallback(event):    
    str = "%s event '%s' received from device [%s]: %s"
    print(str % (event.format, event.event, event.device, json.dumps(event.data)))
    print(event.timestamp)
    if event.device == 'SensorHome:D001':
        insertD001(event.event, json.dumps(event.data), event.timestamp)
    if event.device == 'SensorHome:D002':
        insertD002(event.event, json.dumps(event.data), event.timestamp)
    if event.device == 'SensorHome:D003':
        insertD003(event.event, json.dumps(event.data), event.timestamp)
        
    
        

myClient.connect()
myClient.deviceEventCallback = myEventCallback
myClient.subscribeToDeviceEvents()
call('python ./fetchData.py', shell=True)





