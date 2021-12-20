import RPi.GPIO as GPIO
from time import*
from firebase import firebase

firebase = firebase.FirebaseApplication('https://raspi1-embebidos-default-rtdb.firebaseio.com/', None)

bt1 = 22
bt2 = 27
ld1 = 12
ld2 = 14

def led1():
 firebase.put("/Led", "/led1", not(GPIO.input(ld1)))
 GPIO.output(ld1,not(GPIO.input(ld1)))
def led2():
 firebase.put("/Led", "/led2", not(GPIO.input(ld2)))
 GPIO.output(ld2,not(GPIO.input(ld2)))

def peripheral_setup():
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(bt1, GPIO.IN, GPIO.PUD_DOWN)
 GPIO.setup(bt2, GPIO.IN, GPIO.PUD_DOWN)
 GPIO.setup(ld1, GPIO.OUT)
 GPIO.setup(ld2, GPIO.OUT)

 GPIO.add_event_detect(ld1,GPIO.Falling,led1,bouncetime=30)
 GPIO.add_event_detect(ld2,GPIO.Falling,led2,bouncetime=30)



def main () :

# Setup
 peripheral_setup()

# Infinite loop
 try:
  while 1 :  
   pass
 except(KeyboardInterrupt,SystemExit):
  print ("BYE")
  GPIO.cleanup()
# Command line execution
if __name__ == '__main__' :
   main()
