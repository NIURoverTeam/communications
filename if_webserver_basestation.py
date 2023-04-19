# I promise I'll document all of this later!
# - Waverly Sonntag
from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler, HTTPServer
import time
from os.path import exists, splitext
import socket

web_host_name = "localhost" # is genuinely localhost
web_port = 8081

tcp_port = 8082
tcp_host_name = "192.168.1.123" # would be the Jetson's hardcoded IP address


class my_server(BaseHTTPRequestHandler):
   def do_GET(self):
      if self.path == '/':
         self.path = '/index.html'
      existy = exists('frontend' + self.path)
      if (existy):
         self.send_response(200)
         exty = splitext(self.path)[1]
         if (exty == '.html'):
            self.send_header("Content-type", "text/html")
         elif (exty == '.svg'):
            self.send_header("Content-type", "image/svg+xml")
         elif (exty == '.css'):
            self.send_header("Content-type", "text/css")
         elif (exty == '.js'):
            self.send_header("Content-type", "text/javascript")
         else:
            self.send_header("content-type", "application/octet-stream")
         self.end_headers()
         f = open('frontend' + self.path, 'r')
         self.wfile.write(bytes(f.read(), 'utf-8'))
      else:
         self.send_response(404)
         self.send_header("Content-type", "text/plain")
         self.end_headers()
         self.wfile.write(bytes('404', 'utf-8'))
   def do_POST(self):
      if (self.path.startswith("/reportstate")):
         tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         print("TCP client initialized.")
         # make TCP connection
         try:
            tcp_client.connect((tcp_host_name, tcp_port))
            tcp_client.sendall(bytes(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'), 'utf-8'))

            received = tcp_client.recv(1024)
         except Exception as e:
            received = '!'.encode()
            print(e)
         finally:
            tcp_client.close()
            print("TCP session done")

         self.send_response(200)
         self.send_header("Content-type", "text/plain")
         self.end_headers()
         self.wfile.write(bytes(received.decode(), 'utf-8'))
         #self.wfile.write(bytes(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'), 'utf-8'))
      else:
         self.send_response(404)
         self.send_header("Content-type", "text/plain")
         self.end_headers()
         self.wfile.write(bytes("404", "utf-8"))

if __name__ == "__main__":
   web_server = HTTPServer((web_host_name, web_port), my_server)
   print("HTTP server started http://%s:%s" % (web_host_name, web_port))

   try:
      web_server.serve_forever()
   except KeyboardInterrupt:
      pass

   web_server.server_close()
   print("Webserver stopped.")
