#!/usr/bin/env python
__author__ = 'skunda'
# This program logs a Raspberry Pi's CPU temperature to a Thingspeak Channel
# To use, get a Thingspeak.com account, set up a channel, and capture the Channel Key at https://thingspeak.com/docs/tutorials/ 
# Then paste your channel ID in the code for the value of "key" below.
# Then run as sudo python pitemp.py (access to the CPU temp requires sudo access)
# You can see my channel at https://thingspeak.com/channels/41518

import http.client
import urllib.parse
import urllib.request
import json
import time
import RPi.GPIO as GPIO ## Import GPIO library
'''-------------LED BLINKING-----------------------------'''
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
#set GPIO Pins
GPIO_TRIGGER = 16
GPIO_ECHO = 18
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
GPIO.output(7,True) ## Turn on GPIO pin 7

sleep = 20 # how many seconds to sleep between posts to the channel
key = 'W9QA2JG71BQV4DXT'  # Thingspeak channel to update

READ_API_KEY='SS9IC5D8E6ITU614'
CHANNEL_ID='304480'

#Report Raspberry Pi internal temperature to Thingspeak Channel
'''----------------------------Distance--------------------------------------------'''
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    dis = (TimeElapsed * 34300) / 2
    distance=round(dis)
    return distance

'''-------------------DATA sending to ThingSpeak-----------------------------------'''
def sending():
    while True:
        #Calculate CPU temperature of Raspberry Pi in Degrees C
        dis=distance()
        print(dis)
        #temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 # Get Raspberry Pi CPU temp
        params = urllib.parse.urlencode({'field3': dis, 'key':key}) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            #print (temp)
            print (response.status, response.reason)
            data = response.read()
            #conn.close()
        except:
            print ("connection failed")
        break

'''-------------------DATA receiving from ThingSpeak-----------------------------------'''
def receiving():
    conn=urllib.request.urlopen('http://api.thingspeak.com/channels/304480/feeds/last.json?api_key=SS9IC5D8E6ITU614')
    response = conn.read()
    print(response)
    print("http status code=%s" % (conn.getcode()))
    data=json.loads(response.decode("utf-8"))
    print (data['field3'],data['created_at'])
    reqData = data['field3']
    print("data received=",(reqData))
    #print(reqData)
    conn.close()


'''------------------- Getting Feedback From ThingSpeak------------------------------'''
def feedback():
    reply=urllib.request.urlopen('http://api.thingspeak.com/apps/thinghttp/send_request?api_key=YKM96EL1LTWKBPAX')
    response = reply.read()
    check=response.decode()
    #print(response)
    return check
    #print (check)
   
#if __name__ == "__main__":

while True:
            sending()
            #print(distance())
            receiving()
            time.sleep(1)
            print('Feedback start')
            c=feedback()
            print("feedback = %s"%c)
            if int(c)!=0: # 
                print('STOP')
                GPIO.output(7,False) ## Turn off GPIO pin 7
                break
            time.sleep(5)


