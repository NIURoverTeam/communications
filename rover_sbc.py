import socketserver
import time
import serial

hit = time.process_time()
hit_prior = hit

#arduino = serial.Serial('/dev/cu.usbmodem14101', 9600, timeout=.5)
#arduino.open()
arduino = serial.Serial('/dev/cu.usbmodem14101', 9600, timeout=.01)

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

      #print(''.join('%01x'%i for i in narr))
      resultantbyte = 0
      for i in narr:
         resultantbyte = (resultantbyte << 4) | i

      #resultantbyte = (narr[0] << 4) & narr[1]
      print('%02x'%resultantbyte)

      

      arduino.write(bytes([resultantbyte]))
      weh = arduino.read(5)
      print(weh)

if __name__ == "__main__":
   HOST, PORT = "localhost", 8082

   tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

   tcp_server.serve_forever()
