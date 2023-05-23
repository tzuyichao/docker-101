from prometheus_client import make_wsgi_app, Counter
from wsgiref.simple_server import make_server

REQUESTS = Counter('hello_worlds_total', 'Hello Worlds requested.', labelnames=['path'])

REQUESTS.labels('/foo')
REQUESTS.labels('/bar')

metrics_app = make_wsgi_app()

def my_app(environ, start_fn):
    if environ['PATH_INFO'] == '/metrics':
        return metrics_app(environ, start_fn)
    elif environ['PATH_INFO'] == '/bar':
        REQUESTS.labels('/bar').inc()
        start_fn('200 OK', [('Content-Type', 'text/plain')])
        return [b'Hello bar World']
    elif environ['PATH_INFO'] == '/foo':
        REQUESTS.labels('/foo').inc()
        start_fn('200 OK', [('Content-Type', 'text/plain')])
        return [b'Hello foo World']
    else:
        start_fn('200 OK', [('Content-Type', 'text/plain')])
        return [b'Hello World']

if __name__ == '__main__':
    httpd = make_server('', 8000, my_app)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
