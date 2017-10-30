import http.client
import urllib.parse
import urllib.request
import json
import time
import RPi.GPIO as GPIO ## Import GPIO library
'''-------------LED BLINKING-----------------------------'''
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
GPIO.output(7,True) ## Turn on GPIO pin 7

sleep = 40 # how many seconds to sleep between posts to the channel
key = 'W9QA2JG71BQV4DXT'  # Thingspeak channel to update

READ_API_KEY='SS9IC5D8E6ITU614'
CHANNEL_ID='304480'

#Report Raspberry Pi internal temperature to Thingspeak Channel
entry_ID=0
'''-------------------DATA sending to ThingSpeak-----------------------------------'''
def sending():
    while True:
        #Calculate CPU temperature of Raspberry Pi in Degrees C
        
        temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 # Get Raspberry Pi CPU temp
        params = urllib.parse.urlencode({'field3': 15, 'key':key}) 
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
def receiving(ID):
    conn=urllib.request.urlopen('http://api.thingspeak.com/channels/307330/feeds/last.json?api_key=PC6IJA1RHOON7UY4')
    response = conn.read()
    print("http status code=%s" % (conn.getcode()))
    check=len(response)
    print(len(response))
    pre_entry=ID
    print('pre_entry=',pre_entry)
    data=json.loads(response.decode("utf-8"))
    #entry_ID = data['entry_id']
    
    if check>4:
        data=json.loads(response.decode("utf-8"))
        entry_ID = data['entry_id']
    else:
        entry_ID=ID
    
    conn.close()
    return entry_ID


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
            time.sleep(20)
            sending()
            
            last=entry_ID 
            entry_ID=receiving(entry_ID)
            print('post_entry_ID=',entry_ID)
            if last!=entry_ID:
                print('blah...blah')
                last=entry_ID
                print('waiting')
                time.sleep(5)
            time.sleep(20)
            
            #print('Feedback start')
            #c=feedback()
            #print(c)
            #if int(c)!=0: # condition is not satisfied
                #print('STOP')
                #GPIO.output(7,False) ## Turn off GPIO pin 7
                #break
            #time.sleep(2)
                                  

