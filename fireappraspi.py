
# !/usr/bin/env python3
#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket

import RPi.GPIO as GPIO
from time import*
from firebase import firebase

firebase = firebase.FirebaseApplication('https://raspi1-embebidos-default-rtdb.firebaseio.com/', None)

led1 = 20
led2 = 21

bajo1 = 22
medio1 = 27
alto1 = 17

alto2 = 23
medio2 = 24
bajo2 = 25

def my_callback1():
 GPIO.output(led1,True)
 GPIO.output(led2,False)
 firebase.put("/Bomba1" , "/bomba1", GPIO.input(led1))
 firebase.put("/Bomba1", "/hora endendido bomba1", strftime("%H:%M"))
 firebase.put("/Bomba2", "/bomba2", GPIO.input(led2))
 firebase.put("/Bomba2", "/hora apagado bomba2", strftime("%H:%M"))
 
def my_callback2():
 GPIO.output(led1,False)
 GPIO.output(led2,True)
 firebase.put("/Bomba1", "/bomba1", GPIO.input(led1))
 firebase.put("/Bomba1", "/hora apagado bomba1", strftime("%H:%M"))
 firebase.put("/Bomba2", "/bomba2", GPIO.input(led2))
 firebase.put("/Bomba2", "/hora encendido bomba2", strftime("%H:%M"))
 
def nivelbajo1():
 firebase.put("/Tanque1", "/bajo1", GPIO.input(bajo1))

def nivelmedio1():
 firebase.put("/Tanque1", "/medio1", GPIO.input(medio1))

def nivelalto1():
 firebase.put("/Tanque1", "/alto1", GPIO.input(alto1))


def nivelbajo2():
 firebase.put("/Tanque2", "/bajo2", GPIO.input(bajo2))

def nivelmedio2():
 firebase.put("/Tanque2", "/medio2", GPIO.input(medio2))

def nivelalto2():
 firebase.put("/Tanque2", "/alto2", GPIO.input(alto2))


def peripheral_setup():
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(led1, GPIO.OUT)
 GPIO.setup(led2, GPIO.OUT)
 GPIO.setup(bajo1, GPIO.IN, GPIO.PUD_DOWN)
 GPIO.setup(bajo2, GPIO.IN, GPIO.PUD_DOWN)
 GPIO.setup(medio1, GPIO.IN, GPIO.PUD_DOWN)
 GPIO.setup(medio2, GPIO.IN, GPIO.PUD_DOWN)
 GPIO.setup(alto1, GPIO.IN, GPIO.PUD_DOWN)
 GPIO.setup(alto2, GPIO.IN, GPIO.PUD_DOWN)

 GPIO.add_event_detect(bajo1,GPIO.BOTH,nivelbajo1,bouncetime=30)
 GPIO.add_event_detect(bajo2,GPIO.BOTH,nivelbajo2,bouncetime=30)

 GPIO.add_event_detect(medio1,GPIO.BOTH,nivelmedio1,bouncetime=30)
 GPIO.add_event_detect(medio2,GPIO.BOTH,nivelmedio2,bouncetime=30)

 GPIO.add_event_detect(alto1,GPIO.BOTH,nivelalto1,bouncetime=30)
 GPIO.add_event_detect(alto2,GPIO.BOTH,nivelalto2,bouncetime=30)

def mysleep(delay): 
 start = time() 
 while time()-start < delay:
  pass

def servidor():
 Request = None

 class RequestHandler_httpd(BaseHTTPRequestHandler):
   def do_GET(self):
    global Request

    messagetosend = bytes('Solicitando',"utf")
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.send_header('Content-Length', len(messagetosend))
    self.end_headers()
    self.wfile.write(messagetosend)
    Request = self.requestline
    Request = Request[5 : int(len(Request)-9)]
    #print(Request)
    if Request == 'on1':
      my_callback1()
      print('bomba1 encendida')
      GPIO.output(led1,True)
      GPIO.output(led2,False)
      
    if Request == 'on2':
      my_callback2()
      print('bomba2 encendida')
      GPIO.output(led2,True)
      GPIO.output(led1,False)
      
    
 server_address_httpd = ('192.168.0.128',8001)
 httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
 print('conectando a servidor')
 print(httpd.fileno())
 httpd.serve_forever()



def main () :

# Setup
 peripheral_setup()

# Infinite loop
 try:
  while 1 :  
   servidor()
   print("listo..")
 except(KeyboardInterrupt,SystemExit):
  print ("BYE")
  GPIO.cleanup()
# Command line execution
if __name__ == '__main__' :
   main()
