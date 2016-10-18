
import RPi.GPIO as GPIO
import threading
from time import sleep

                  # GPIO Ports
Enc_0_A = 1              # Encoder input A: input GPIO 2 
Enc_0_B = 0                   # Encoder input B: input GPIO 3

Enc_1_A = 21             # Encoder input A: input GPIO 2 
Enc_1_B = 20                   # Encoder input B: input GPIO 3

Enc_2_A = 14              # Encoder input A: input GPIO 2 
Enc_2_B = 15                 # Encoder input B: input GPIO 3

Enc_3_A = 2              # Encoder input A: input GPIO 2 
Enc_3_B = 3                   # Encoder input B: input GPIO 3



Rotary_counter_0 = 0           # Start counting from 0
Current_0_A = 1               # Assume that rotary switch is not 
Current_0_B = 1               # moving while we init software
LockRotary_0 = threading.Lock()      # create lock for rotary switch


Rotary_counter_1 = 0           # Start counting from 0
Current_1_A = 1               # Assume that rotary switch is not 
Current_1_B = 1               # moving while we init software
LockRotary_1 = threading.Lock()      # create lock for rotary switch
   
Rotary_counter_2 = 0           # Start counting from 0
Current_2_A = 1               # Assume that rotary switch is not 
Current_2_B = 1               # moving while we init software
LockRotary_2 = threading.Lock()      # create lock for rotary switch

Rotary_counter_3 = 0           # Start counting from 0
Current_3_A = 1               # Assume that rotary switch is not 
Current_3_B = 1               # moving while we init software
LockRotary_3 = threading.Lock()      # create lock for rotary switch

# initialize interrupt handlers
def init():
   GPIO.setwarnings(True)
   GPIO.setmode(GPIO.BCM)               # Use BCM mode
                                 # define the Encoder switch inputs
   GPIO.setup(Enc_0_A, GPIO.IN)             
   GPIO.setup(Enc_0_B, GPIO.IN)
   GPIO.setup(Enc_1_A, GPIO.IN)             
   GPIO.setup(Enc_1_B, GPIO.IN)
   GPIO.setup(Enc_2_A, GPIO.IN)             
   GPIO.setup(Enc_2_B, GPIO.IN)
   GPIO.setup(Enc_3_A, GPIO.IN)             
   GPIO.setup(Enc_3_B, GPIO.IN)


                                 # setup callback thread for the A and B encoder 
                                 # use interrupts for all inputs
   GPIO.add_event_detect(Enc_0_A, GPIO.RISING, callback=rotary_interrupt_0)             # NO bouncetime 
   GPIO.add_event_detect(Enc_0_B, GPIO.RISING, callback=rotary_interrupt_0)             # NO bouncetime 
   GPIO.add_event_detect(Enc_1_A, GPIO.RISING, callback=rotary_interrupt_1)             # NO bouncetime 
   GPIO.add_event_detect(Enc_1_B, GPIO.RISING, callback=rotary_interrupt_1)             # NO bouncetime 
   GPIO.add_event_detect(Enc_2_A, GPIO.RISING, callback=rotary_interrupt_2)             # NO bouncetime 
   GPIO.add_event_detect(Enc_2_B, GPIO.RISING, callback=rotary_interrupt_2)             # NO bouncetime 
   GPIO.add_event_detect(Enc_3_A, GPIO.RISING, callback=rotary_interrupt_3)             # NO bouncetime 
   GPIO.add_event_detect(Enc_3_B, GPIO.RISING, callback=rotary_interrupt_3)             # NO bouncetime 

   return



# Rotarty encoder interrupt:
# this one is called for both inputs from rotary switch (A and B)
def rotary_interrupt_0(A_or_B):
   global Rotary_counter_0, Current_0_A, Current_0_B, LockRotary_0
                                       # read both of the switches
   Switch_A = GPIO.input(Enc_0_A)
   Switch_B = GPIO.input(Enc_0_B)
                                       # now check if state of A or B has changed
                                       # if not that means that bouncing caused it
   if Current_0_A == Switch_A and Current_0_B == Switch_B:      # Same interrupt as before (Bouncing)?
      return                              # ignore interrupt!

   Current_0_A = Switch_A                        # remember new state
   Current_0_B = Switch_B                        # for next bouncing check


   if (Switch_A and Switch_B):                  # Both one active? Yes -> end of sequence
      LockRotary_0.acquire()                  # get lock 
      if A_or_B == Enc_B:                     # Turning direction depends on 
         Rotary_counter_0 += 1                  # which input gave last interrupt
      else:                              # so depending on direction either
         Rotary_counter_0 -= 1                  # increase or decrease counter
      LockRotary_0.release()                  # and release lock
   return                                 # THAT'S IT

# Main loop. Demonstrate reading, direction and speed of turning left/rignt
def main():
   global Rotary_counter_0, LockRotary_0
   

   Volume = 0                           # Current Volume   
   NewCounter = 0                        # for faster reading with locks
   cnt = 0               
   speed = 0
   init()                              # Init interrupts, GPIO, ...
            
   while True :                        # start test 
      sleep(0.1)                        # sleep 100 msec
      cnt = cnt +1
                                    # because of threading make sure no thread
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         # changes value until we get them
                                    # and reset them
                                    
      LockRotary_0.acquire()               # get lock for rotary switch
      NewCounter = Rotary_counter_0         # get counter value
      Rotary_counter_0 = 0                  # RESET IT TO 0
      LockRotary_0.release()               # and release lock
               
      if (NewCounter !=0):               # Counter has CHANGED
         Volume = Volume + NewCounter

                                 
      if (cnt > 10):
        speed = (Volume /cnt)
	print speed
	cnt = 0
	Volume = 0

# start main demo function
main()
