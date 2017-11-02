#!/usr/bin/env python
import RPi.GPIO as GPIO
import PCA9685 as servo
import video_dir as US_turn
#import PCA9685 as p
import time    # Import necessary modules
'''        cloud code          '''
import http.client
import urllib.parse
import urllib.request
import json
import time
import RPi.GPIO as GPIO ## Import GPIO library
key = 'W9QA2JG71BQV4DXT'  # Thingspeak channel to update
READ_API_KEY='PC6IJA1RHOON7UY4'
CHANNEL_ID='306964'
entry_ID=0
'''Initializing Observation Sequence Number'''
conn=urllib.request.urlopen('http://api.thingspeak.com/channels/307330/feeds/last.json?api_key=PC6IJA1RHOON7UY4')
response = conn.read()
print("http status code=%s" % (conn.getcode()))
check=len(response)
print(len(response))
pre_entry=entry_ID
print('pre_entry=',pre_entry)
data=json.loads(response.decode("utf-8"))
        #entry_ID = data['entry_id']
    
if check>4: # means data received 
        data=json.loads(response.decode("utf-8"))
        entry_ID = data['entry_id']
else: # means data did not get received 
        entry_ID=pre_entry
    
conn.close()
#-----------------------------------------------------------------#
#Report Raspberry Pi internal temperature to Thingspeak Channel
'''-------------------DATA  to ThingSpeak-----------------------------------'''
def sending(distance):
    while True:
        params = urllib.parse.urlencode({'field3': distance, 'key':key}) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")

        '''try:
                conn.request("POST",'http://api.thingspeak.com/update/?key=W9QA2JG71BQV4DXT&field1=D')
                response = conn.getresponse()
                print (response.status, response.reason)
                #data = response.read()'''
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print (response.status, response.reason)
            data = response.read()
            #print(data)
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
    
        if check>4: # means data received 
                data=json.loads(response.decode("utf-8"))
                entry_ID = data['entry_id']
        else: # means data did not get received 
                entry_ID=ID
    
        conn.close()
        return entry_ID




# ===========================================================================
# Raspberry Pi pin11, 12, 13 and 15 to realize the clockwise/counterclockwise
# rotation and forward and backward movements
# ===========================================================================
Motor0_A = 11  # pin11
Motor0_B = 12  # pin12
Motor1_A = 13  # pin13
Motor1_B = 15  # pin15

# ===========================================================================
# Set channel 4 and 5 of the servo driver IC to generate PWM, thus 
# controlling the speed of the car
# ===========================================================================
EN_M0    = 4  # servo driver IC CH4
EN_M1    = 5  # servo driver IC CH5

pins = [Motor0_A, Motor0_B, Motor1_A, Motor1_B]

# ===========================================================================
# Adjust the duty cycle of the square waves output from channel 4 and 5 of
# the servo driver IC, so as to control the speed of the car.
# ===========================================================================
def setSpeed(speed):
        speed *= 40
        #print ('speed is: ', speed)
        pwm.write(EN_M0, 0, speed)
        pwm.write(EN_M1, 0, speed)

def setup(busnum=None):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)        # Number GPIOs by its physical location
        
        ###################  set GPIO Pins for US sensor
        global GPIO_TRIGGER, GPIO_ECHO
        GPIO_TRIGGER = 16
        GPIO_ECHO = 18
         
        #set GPIO direction (IN / OUT)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        ########################################
        global forward0, forward1, backward1, backward0
        global pwm


        
        global leftPWM, rightPWM, homePWM, pwm
        leftPWM = 300
        homePWM = 378 #was 280 now adjusting
        rightPWM = 460
        offset =0
        try:
                for line in open('config'):
                        if line[0:8] == 'offset =':
                                offset = int(line[9:-1])
        except:
                print ('config error')
        leftPWM += offset
        homePWM += offset
        rightPWM += offset
        if busnum == None:
                pwm = servo.PWM()                  # Initialize the servo controller.
        else:
                pwm = servo.PWM(bus_number=busnum) # Initialize the servo controller.
        pwm.frequency = 60
        
        if busnum == None:
                pwm = servo.PWM()                  # Initialize the servo controller.
        else:
                pwm = servo.PWM(bus_number=busnum) # Initialize the servo controller.

        pwm.frequency = 60
        forward0 = 'True'
        forward1 = 'True'
        try:
                for line in open("config"):
                        if line[0:8] == "forward0":
                                forward0 = line[11:-1]
                        if line[0:8] == "forward1":
                                forward1 = line[11:-1]
        except:
                pass
        if forward0 == 'True':
                backward0 = 'False'
        elif forward0 == 'False':
                backward0 = 'True'
        if forward1 == 'True':
                backward1 = 'False'
        elif forward1 == 'False':
                backward1 = 'True'
        for pin in pins:
                GPIO.setup(pin, GPIO.OUT)   # Set all pins' mode as output

# ===========================================================================
# Control the DC motor to make it rotate clockwise, so the car will 
# move forward.
# ===========================================================================
def turn_left():
        global leftPWM
        pwm.write(0, 0, leftPWM)  # CH0

# ==========================================================================================
# Make the car turn right.
# ==========================================================================================
def turn_right():
        global rightPWM
        pwm.write(0, 0, rightPWM)

# ==========================================================================================
# Make the car turn back.
# ==========================================================================================

def turn(angle):
        angle = Map(angle, 0, 255, leftPWM, rightPWM)
        pwm.write(0, 0, angle)

def home():
        global homePWM
        pwm.write(0, 0, homePWM)

def motor0(x):
        if x == 'True':
                GPIO.output(Motor0_A, GPIO.LOW)
                GPIO.output(Motor0_B, GPIO.HIGH)
        elif x == 'False':
                GPIO.output(Motor0_A, GPIO.HIGH)
                GPIO.output(Motor0_B, GPIO.LOW)
        else:
                print ('Config Error')

def motor1(x):
        if x == 'True':
                GPIO.output(Motor1_A, GPIO.LOW)
                GPIO.output(Motor1_B, GPIO.HIGH)
        elif x == 'False':
                GPIO.output(Motor1_A, GPIO.HIGH)
                GPIO.output(Motor1_B, GPIO.LOW)

def forward():
        #print ('forward')
        motor0(forward0)
        motor1(forward1)
        #GPIO.output(11, GPIO.HIGH)
        #GPIO.output(12, GPIO.HIGH)

def backward():
        motor0(backward0)
        motor1(backward1)

def forwardWithSpeed(spd = 50):
        setSpeed(spd)
        motor0(forward0)
        motor1(forward1)

def backwardWithSpeed(spd = 50):
        setSpeed(spd)
        motor0(backward0)
        motor1(backward1)

def stop():
        for pin in pins:
                GPIO.output(pin, GPIO.LOW)

# ===========================================================================
# The first parameter(status) is to control the state of the car, to make it 
# stop or run. The parameter(direction) is to control the car's direction 
# (move forward or backward).
# ===========================================================================
def ctrl(status, direction=1):
        if status == 1:   # Run
                if direction == 1:     # Forward
                        forward()
                elif direction == -1:  # Backward
                        backward()
                else:
                        print ('Argument error! direction must be 1 or -1.')
        elif status == 0: # Stop
                stop()
        else:
                print ('Argument error! status must be 0 or 1.')

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
        distance=round(dis,2)
        return distance


'''while True:
        setup()
        print ('hi')
        setSpeed(60)
        #turn_left()
        forward()
        time.sleep(1.2)

        ######################## this code is turning the ultra sionic
        #US_turn.setup()
        #US_turn.home_x_y()
        #time.sleep(1)
        #US_turn.turn_right()
        #time.sleep(2)
        #US_turn.home_x_y()
        #######################
        #forward()
        home()
#        motor1(forward1)
        time.sleep(1.2)
        stop()
        #setSpeed(60)
        #turn_right()
        forward()
        time.sleep(1.2)
        stop()
######################## this code is turning the ultra sionic
        US_turn.setup()
        US_turn.home_x_y()
        time.sleep(1)
        US_turn.turn_right()
        time.sleep(2)
        US_turn.home_x_y()
        #######################    this is the ultrasonic data
        #US_data.distance()
        distance()
        print(distance())
        if distance() < int(20) :    #decision onboard loop
                setSpeed(60)
                turn_left()
                forward()
                time.sleep(1.2)
        else:
                setSpeed(60)
                turn_right()
                forward()
                time.sleep(1.2)
                        
        ########################
        forward()
        home()
        motor1(forward1)
        time.sleep(1.2)
        stop()
        time.sleep(5)'''
setup()
US_turn.setup()
US_turn.home_x_y()
stop()
distance()
distance()
time.sleep(2)
while True:
    try:
        #'''
        setSpeed(50)
        home()
        forward()
        #stop()
        D_straight = distance()
        print("Straight distance = %f" %D_straight)

        if D_straight<40:
                stop()
                US_turn.turn_right()
                time.sleep(1)
                D_right = distance()
                print(D_right)
                sending(D_right)
                last=entry_ID
                print("receiving", last)
                time.sleep(.5)
                entry_ID=receiving(entry_ID)
                time.sleep(.5)
                print("post receiving=", entry_ID)
                print("Right distance = %f" %D_right)
                time.sleep(.25)
                US_turn.turn_home()
                time.sleep(.25)
                if last != entry_ID: # find an obstacle
                        print("turning left")
                        last=entry_ID
                        setSpeed(50)
                        turn_left()
                        forward()
                        time.sleep(1.3)
                        home()                        
                else:
                        print("turning right")
                        setSpeed(50)
                        turn_right()
                        forward()
                        time.sleep(1.15)
                        home()
                        #stop()
                        
                        #stop()
                '''
                last=entry_ID # reinitiating the RASPBERRY PI
                print('waiting')
                time.sleep(5)'''
        time.sleep(.1)

    except KeyboardInterrupt:
        print("code stopped")
        stop()
        break
        
            
        

