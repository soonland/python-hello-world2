from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        response = requests.get('https://share-a-review.vercel.app/fr')
        soup = BeautifulSoup(response.content, 'html.parser')
        footer = soup.find(attrs={"data-testid": "testid.footer"})
        footer_text = footer.get_text() if footer else 'Footer not found'

        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(footer_text.encode('utf-8'))
