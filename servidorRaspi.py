import os
import socket

from http.server import BaseHTTPRequestHandler, HTTPServer
import RPi.GPIO as GPIO
from time import*

led1 = 20
led2 = 21


myip = socket.gethostbyname(socket.gethostname()))
print (myip)
def peripheral_setup():
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(led1, GPIO.OUT)
 GPIO.setup(led2, GPIO.OUT)
 
 
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
      print('bomba1 encendida')
      GPIO.output(led1,True)
      GPIO.output(led2,False)
      
    if Request == 'on2':
      print('bomba2 encendida')
      GPIO.output(led2,True)
      GPIO.output(led1,False)
      
    
 server_address_httpd = (myip,8001)
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
 except(KeyboardInterrupt,SystemExit):
  print ("BYE")
  GPIO.cleanup()
# Command line execution
if __name__ == '__main__' :
   main()
