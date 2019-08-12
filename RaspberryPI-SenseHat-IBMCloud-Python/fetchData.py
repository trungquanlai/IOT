import mysql.connector
from sense_hat import *
import numpy as np

def connect():
    mydb = mysql.connector.connect(
    host="localhost",
    user="pi",
    passwd="raspberry",
    database="IOTDB"
    )
    return mydb

def fetchLastRecordD001():
    mydb = connect()
    mycursor = mydb.cursor()
    sql = "SELECT value FROM D001 ORDER BY id DESC LIMIT 1"
    
    mycursor.execute(sql)
    fetchData = mycursor.fetchone()
    #print(fetchData)
    if fetchData == None:
        return ""
    else:   
        result = str(fetchData[0])
    return result
	
def fetchLastRecordD002():
    mydb = connect()
    mycursor = mydb.cursor()
    sql = "SELECT value FROM D002 ORDER BY id DESC LIMIT 1"
    
    mycursor.execute(sql)
    fetchData = mycursor.fetchone()
    #print(fetchData)
    if fetchData == None:
        return False
    else:   
        result = str(fetchData[0])
    return result
	
def fetchLastRecordD003():
    mydb = connect()
    mycursor = mydb.cursor()
    sql = "SELECT value FROM D003 ORDER BY id DESC LIMIT 1"
    
    mycursor.execute(sql)
    fetchData = mycursor.fetchone()
    #print(fetchData)
    if fetchData == None:
        return False
    else:   
        result = str(fetchData[0])
    return result

# Draw the foreground (fg) into a numpy array
Rd = (255, 0, 0)
Gn = (0, 255, 0)
Bl = (0, 0, 255)
Gy = (128, 128, 128)
__ = (0, 0, 0)
fg = np.array([
    [__, Rd, Rd, __, Gn, Gn, Gn, __],
    [__, __, Rd, __, __, __, Gn, __],
    [__, __, Rd, __, __, Gn, __, __],
    [__, __, Rd, __, Gn, Gn, Gn, __],
    [Bl, Bl, Bl, __, __, Gy, __, __],
    [__, Bl, Bl, __, Gy, __, Gy, __],
    [__, __, Bl, __, Gy, __, Gy, __],
    [Bl, Bl, Bl, __, __, Gy, Gy, __],
    ], dtype=np.uint8)
# Mask is a boolean array of which pixels are transparent
mask = np.all(fg == __, axis=2)

def display(hat, selection):
    # Draw the background (bg) selection box into another numpy array
    left, top, right, bottom = {
        '1': (0, 0, 4, 4),
        '2': (4, 0, 8, 4),
        'Q': (4, 4, 8, 8),
        '3': (0, 4, 4, 8),
        }[selection]
    bg = np.zeros((8, 8, 3), dtype=np.uint8)
    bg[top:bottom, left:right, :] = (255, 255, 255)
    # Construct final pixels from bg array with non-transparent elements of
    # the menu array
    hat.set_pixels([
        bg_pix if mask_pix else fg_pix
        for (bg_pix, mask_pix, fg_pix) in zip(
            (p for row in bg for p in row),
            (p for row in mask for p in row),
            (p for row in fg for p in row),
            )
        ])

def execute(hat, selection):
    if selection == '1':
        value = fetchLastRecordD001()
        if value == False:
            return True
        else:
            hat.show_message(value)
    elif selection == '2':
        value = fetchLastRecordD002()
        if value == False:
            return True
        else:
            hat.show_message(value)     
    elif selection == '3':
        value = fetchLastRecordD003()
        if value == False:
            return True
        else:
            hat.show_message(value)
    else:
        return True
    return False

def move(selection, direction):
    return {
        ('1', DIRECTION_RIGHT): '2',
        ('1', DIRECTION_DOWN):  '3',
        ('2', DIRECTION_LEFT):  '1',
        ('2', DIRECTION_DOWN):  'Q',
        ('Q', DIRECTION_UP):    '2',
        ('Q', DIRECTION_LEFT):  '3',
        ('3', DIRECTION_RIGHT): 'Q',
        ('3', DIRECTION_UP):    '1',
        }.get((selection, direction), selection)

def main():
    hat = SenseHat()
    selection = '1'
    while True:
        display(hat, selection)
        event = hat.stick.wait_for_event()
        if event.action == ACTION_PRESSED:
            if event.direction == DIRECTION_MIDDLE:
                if execute(hat, selection):
                    break
            else:
                selection = move(selection, event.direction)
    hat.clear()
    
main()
