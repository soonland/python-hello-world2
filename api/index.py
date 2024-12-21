from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        response = requests.get('https://www.youtube.com/watch?v=nN6VR92V70M')
        # soup = BeautifulSoup(response.content, 'html.parser')
        # title = soup.find('title')
        # title_text = title.get_text() if title else 'Title not found'

        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(response.content.encode('utf-8'))
