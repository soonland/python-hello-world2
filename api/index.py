from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        response = requests.get('https://www.youtube.com/watch?v=7SVBjn4oBBA')
        response_text = response.text

        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(response_text.encode('utf-8'))
