from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Parse the URL and extract query parameters
        query_components = parse_qs(urlparse(self.path).query)
        video_id = query_components.get("video_id", [None])[0]

        if video_id:
            try:
                # Attempt to fetch French captions
                transcript = YouTubeTranscriptApi.get_transcript(
                    video_id, languages=['fr'])
            except NoTranscriptFound:
                # Fallback to any available language if French is unavailable
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(video_id)
                except NoTranscriptFound:
                    self._send_response(
                        {"error": "No transcript available for this video in any language."},
                        status=404
                    )
                    return
            except TranscriptsDisabled:
                self._send_response(
                    {"error": "Transcripts are disabled for this video."},
                    status=403
                )
                return
            except VideoUnavailable:
                self._send_response(
                    {"error": "The video is unavailable. Please check the video ID."},
                    status=404
                )
                return
            except Exception as e:
                # Catch any other errors
                self._send_response(
                    {"error": "An unexpected error occurred.",
                        "details": str(e)},
                    status=500
                )
                return

            # Successfully retrieved transcript
            self._send_response(transcript, status=200)
        else:
            # Return an error if the `video_id` parameter is missing
            self._send_response(
                {"error": "Please provide a video_id as a query parameter."},
                status=400
            )

    def _send_response(self, data, status=200):
        """
        Helper method to send an HTTP response with the given status code and data.
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
