import RPi.GPIO as GPIO
from time import*
from firebase import firebase

firebase = firebase.FirebaseApplication('https://raspi1-embebidos-default-rtdb.firebaseio.com/', None)

bajo1 = 22
medio1 = 27

def nivelbajo1():
 firebase.put("/Tanque1", "/bajo1", GPIO.input(bajo1))

def nivelmedio1():
 firebase.put("/Tanque1", "/medio1", GPIO.input(medio1))


def peripheral_setup():
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(bajo1, GPIO.IN, GPIO.PUD_DOWN)
 GPIO.setup(medio1, GPIO.IN, GPIO.PUD_DOWN)

 GPIO.add_event_detect(bajo1,GPIO.BOTH,nivelbajo1,bouncetime=30)
 GPIO.add_event_detect(medio1,GPIO.BOTH,nivelmedio1,bouncetime=30)



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
