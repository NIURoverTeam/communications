import socketserver
import time
#import serial

hit = time.process_time()
hit_prior = hit

def convert_basestation_values_to_arduino_values(number):
   return int((float(number) / 0.2)) + 0x7

class Handler_TCPServer(socketserver.BaseRequestHandler):
   def handle(self):
      global hit
      global hit_prior
      hit_prior = hit
      hit = time.process_time()
      print("Time elapsed since last req: ", (hit-hit_prior))
      self.data = self.request.recv(1024).strip()
      print("{} sent:".format(self.client_address[0]))
      #print(self.data)
      self.request.sendall("ACK from TCP Server".encode())

      arr = str(self.data)[2:-1].split(',')
      narr = map(convert_basestation_values_to_arduino_values, arr)

      print(''.join('%01x'%i for i in narr))

      

      #arduino = serial.Serial('/dev/tty#', 9600, timeout=.1)
      #arduino.write(

if __name__ == "__main__":
   HOST, PORT = "localhost", 8082

   tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

   tcp_server.serve_forever()
