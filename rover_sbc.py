import socketserver
import time

hit = time.process_time()
hit_prior = hit

class Handler_TCPServer(socketserver.BaseRequestHandler):
   def handle(self):
      global hit
      global hit_prior
      hit_prior = hit
      hit = time.process_time()
      print("Time elapsed since last req: ", (hit-hit_prior))
      self.data = self.request.recv(1024).strip()
      print("{} sent:".format(self.client_address[0]))
      print(self.data)
      self.request.sendall("ACK from TCP Server".encode())

if __name__ == "__main__":
   HOST, PORT = "localhost", 8082

   tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

   tcp_server.serve_forever()
