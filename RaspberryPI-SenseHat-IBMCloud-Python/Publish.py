import ibmiotf.application
from sense_hat import SenseHat
from time import time
from time import sleep

sense = SenseHat()

options = {
    "org": "sr7gke",
    "id": "D001",
    "auth-method": "token",
    "auth-key": "a-sr7gke-peofyfalld",
    "auth-token": "0EhF(z4xL9NwlxchVh",
    "port": 8883,
    "keepalive": 60,
  }  

myClient = ibmiotf.application.Client(options)

myClient.connect()

while True:
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()
    
    
    myData={"Temperature" : sense.get_temperature(), "Humidity" : humidity, "Pressure" : pressure}
    print(myData)    
    
    myClient.publishEvent("SensorHome","D001","PreTemHu","json", myData)    

    for event in sense.stick.get_events():
        joyStickEventData={"Direction" : event.direction, "Action" : event.action}
        print(joyStickEventData)        
        myClient.publishEvent("SensorHome","D002","joyStickEvent","json", joyStickEventData)
        

    orientation_data = sense.get_orientation()
    pitch = orientation_data['pitch']    
    yaw = orientation_data['yaw']
    roll = orientation_data['roll']    
    
    orientationData={"Pitch" : orientation_data['pitch'], "Yaw" : orientation_data['yaw'], "Roll" : orientation_data['roll']}
    print(orientationData)
        
    myClient.publishEvent("SensorHome","D003","Orientation","json", orientationData)
    sleep(1)
