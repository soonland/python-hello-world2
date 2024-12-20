from http.server import BaseHTTPRequestHandler
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from urllib.parse import urlparse, parse_qs
import json


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        action = query_components.get('action', [None])[0]

        if action == 'get_transcript':
            self.get_transcript(query_components)
        elif action == 'list_transcripts':
            self.list_transcripts(query_components)
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write("Bad Request, no action".encode())
        return

    def get_transcript(self, query_components):
        video_id = query_components.get('videoId', [None])[0]
        if video_id:
            formatter = JSONFormatter()
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id, languages=['fr', 'en'])
            json_formatted = formatter.format_transcript(transcript)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(json_formatted).encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write("Bad Request, no video id".encode())

    def list_transcripts(self, query_components):
        video_id = query_components.get('videoId', [None])[0]
        if video_id:
            transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript_list = [t.language for t in transcripts]
            json_formatted = JSONFormatter().format_transcript(transcript_list)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(json_formatted).encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write("Bad Request, no video id".encode())
