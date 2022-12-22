import os
import socket

from http.server import BaseHTTPRequestHandler, HTTPServer
import RPi.GPIO as GPIO
from time import*

led1 = 12
led2 = 4
stado=""

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
myip = s.getsockname()[0]
puerto = 9901
print (str(myip)+":"+str(puerto))



def peripheral_setup():
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(led1, GPIO.OUT)
 GPIO.setup(led2, GPIO.OUT)
 
 
def servidor():
 Request = None

 class RequestHandler_httpd(BaseHTTPRequestHandler):
   def do_GET(self):
    global Request


    Request = self.requestline
    Request = Request[5 : int(len(Request)-9)]
    #print(Request)
    if Request == 'on1':
      stado = 'led1 encendido'
      print(stado)
      GPIO.output(led1,True)
      
    if Request == 'on2':
      stado='led2 encendido'
      print(stado)
      GPIO.output(led2,True)

     if Request == 'off1':
      stado='led1 apagado'
      print(stado)
      GPIO.output(led1,False)
      
    if Request == 'off2':
      stado='led2 apagado'
      print(stado)
      GPIO.output(led2,False)

    messagetosend = bytes(stado,"utf")
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.send_header('Content-Length', len(messagetosend))
    self.end_headers()
    self.wfile.write(messagetosend)
    
    
 server_address_httpd = (myip,puerto) #utilizar diferentes puertos para cada raspberry
 httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
 print('conectando a servidor')
 #print(httpd.fileno())
 httpd.serve_forever()
 
 
 
def main () :

# Setup
 peripheral_setup()

# Infinite loop
 try:
  while 1 :  
   servidor()
 except(KeyboardInterrupt,SystemExit):
  print ("Servidor detenido")
  GPIO.cleanup()
# Command line execution
if __name__ == '__main__' :
   main()
