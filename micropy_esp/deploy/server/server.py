#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from os import curdir, sep
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

IP_MAP = {
    'georgi':'ws://192.168.1.5:8266/'
}
class Server(HTTPServer):
    def __init__(self,arg,arg1):
        HTTPServer.__init__(self,arg,arg1)
        print('Scanning network for Connected devices')
        import subprocess
        p = subprocess.Popen("arp-scan -l | grep ec:fa:bc:13:61:a4", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        if output:
            print("Yay, the devine is connected to your network!")
        else:
            print("The device is not present!")

class S(BaseHTTPRequestHandler):

    def do_GET(self):

        try:
            # Check the file extension required and
            # set the right mime type

            sendReply = False
            if 'connect' in self.path:
                print(self.path)
                user = self.path.split('?')[1]
                url = IP_MAP[user]
                mimetype = 'text/plain'
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(url.encode())
                return
    
            if self.path == "/":
                self.path = "/index.html"
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype = 'image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype = 'image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype = 'application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype = 'text/css'
                sendReply = True

            if sendReply == True:
				# Open the static file requested and send it
                f = open(curdir + sep + self.path, 'r')
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(f.read().encode())
                
                f.close()
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=Server, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
