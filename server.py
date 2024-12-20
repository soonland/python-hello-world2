from http.server import HTTPServer
from api.index import handler
import os


def run(server_class=HTTPServer, handler_class=handler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    run(port=port)
