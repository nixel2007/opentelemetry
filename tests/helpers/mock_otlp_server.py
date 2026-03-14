#!/usr/bin/env python3
"""Mock HTTP server for OTLP transport tests.
Responds based on path:
  /v1/traces - 200 OK
  /v1/logs   - 200 OK
  /v1/metrics - 200 OK
  /error     - 500 Internal Server Error
  /retry     - 503 Service Unavailable (first 2 calls), then 200
  /too-many  - 429 Too Many Requests
"""
import http.server
import sys

retry_counts = {}

class OTLPMockHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        self.rfile.read(content_length) if content_length > 0 else b''

        if self.path in ('/v1/traces', '/v1/logs', '/v1/metrics'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{}')
        elif self.path == '/error':
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'error')
        elif self.path == '/retry':
            count = retry_counts.get('/retry', 0) + 1
            retry_counts['/retry'] = count
            if count <= 2:
                self.send_response(503)
                self.end_headers()
                self.wfile.write(b'retry later')
            else:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{}')
                retry_counts['/retry'] = 0
        elif self.path == '/too-many':
            self.send_response(429)
            self.end_headers()
            self.wfile.write(b'too many requests')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 14318
    server = http.server.HTTPServer(('127.0.0.1', port), OTLPMockHandler)
    print(f'Mock OTLP server on port {port}', flush=True)
    server.serve_forever()
