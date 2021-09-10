#!/usr/bin/python
import Jetson.GPIO as GPIO
import time

class Sonar():

    def __init__(self, gpio_trigger, gpio_echo):
    
        GPIO.setmode(GPIO.BOARD)
        
        self._gpio_trigger  = gpio_trigger
        self._gpio_echo     = gpio_echo
       
        self._is_reading    = False
        
        self._speed_sound   = 17150.0 #- divided by 2 in cm/s
        
        self._last_time_reading = 0
        #self._timeout       = range_max/self._speed_sound*2

        GPIO.setup(gpio_trigger, GPIO.OUT)
        GPIO.setup(gpio_echo, GPIO.IN)
        


        #- Waiting for sensor to settle
        GPIO.output(gpio_trigger, GPIO.LOW)
        time.sleep(10)
        

    def get_range(self):
        self._is_reading = True
        #--- Call for a reading
        GPIO.output(self._gpio_trigger, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self._gpio_trigger, GPIO.LOW)
        
        #GPIO.output(self._gpio_trigger, GPIO.HIGH)
        #time.sleep(0.00001)
        #GPIO.output(self._gpio_trigger, GPIO.LOW)

        
        pulse_start_time = time.time()
        pulse_end_time = time.time()
        #--- Wait for the answer
        while GPIO.input(self._gpio_echo)==0:
            pulse_start_time = time.time()
            
        time0= time.time()
        while GPIO.input(self._gpio_echo)==1:
            pulse_end_time = time.time()
            # if time.time() - time0 > self._timeout:
                # self._is_reading = False
                # # print time.time() - time0
                # # print self._timeout
                # # print("TIMEOUT")
                # return (-1)
            
        self._last_time_reading = time.time()
        self._is_reading = False

        pulse_duration = pulse_end_time - pulse_start_time
        distance = pulse_duration * self._speed_sound
        
        #if distance > self._range_max:
            #distance = self._range_max
            
        #if distance < self._range_min:
            #distance = self._range_min
            # distance = -1
            
        return(distance)

    @property
    def is_reading(self):
        return(self._is_reading)
        
if __name__ == "__main__":
    GPIO.setwarnings(False)
    print("cleaning residue readings and starting") 
    GPIO.cleanup() # cleanup all GPIO
    
	#-- FRONT
    FRONT_PIN_TRIGGER = 31
    FRONT_PIN_ECHO = 33

 #-- RIGHT
    RIGHT_PIN_TRIGGER = 19
    RIGHT_PIN_ECHO = 21

    #-- LEFT
    LEFT_PIN_TRIGGER = 16
    LEFT_PIN_ECHO = 18 
   

    left = Sonar(LEFT_PIN_TRIGGER, LEFT_PIN_ECHO)
    right = Sonar(RIGHT_PIN_TRIGGER, RIGHT_PIN_ECHO)
    front = Sonar(FRONT_PIN_TRIGGER, FRONT_PIN_ECHO)
    
    while True:
        l = left.get_range()
        r = right.get_range()
        d = front.get_range()
        lis = [round(l,2),round(d,2),round(r,2)]
        #if d>0: print "Distance = %4.1f cm"%d
        print (lis)

