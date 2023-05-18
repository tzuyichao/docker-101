from prometheus_client import make_wsgi_app
from wsgiref.simple_server import make_server

metrics_app = make_wsgi_app()

def my_app(environ, start_fn):
    if environ['PATH_INFO'] == '/metrics':
        return metrics_app(environ, start_fn)
    else:
        start_fn('200 OK', [('Content-Type', 'text/plain')])
        return [b'Hello World']

if __name__ == '__main__':
    httpd = make_server('', 8000, my_app)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")