import random
from prometheus_client import start_http_server, Counter
import http.server

REQUEST = Counter('hello_world_total', 'Hello World requested.')
EXCEPTIONS = Counter('hello_world_exceptions_total', 'Exceptions serving Hello World.')

class MyHandler(http.server.BaseHTTPRequestHandler):
    @EXCEPTIONS.count_exceptions()
    def do_GET(self):
        REQUEST.inc()
        if random.random() < 0.2:
          raise Exception
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")

if __name__ == '__main__':
    start_http_server(8000)
    server = http.server.HTTPServer(('localhost', 8001), MyHandler)
    server.serve_forever()