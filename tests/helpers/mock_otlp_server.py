#!/usr/bin/env python3
"""Mock HTTP server for OTLP transport tests.
Responds based on path:
  /v1/traces - 200 OK
  /v1/logs   - 200 OK
  /v1/metrics - 200 OK
  /error     - 500 Internal Server Error
  /retry     - 503 Service Unavailable (first 2 calls), then 200
  /too-many  - 429 Too Many Requests
  /retry-after/<seconds> - 429 Too Many Requests with Retry-After: <seconds>
  /retry-after-date/<format>/<seconds> - 429 Too Many Requests with Retry-After: HTTP-date
      <seconds> from now; <format> is imf (IMF-fixdate), rfc850 or asctime (RFC 7231, 7.1.1.1)
  /v1/gzip-traces - 200 OK if Content-Encoding: gzip and body is valid gzip, else 400
  /big-response - 200 OK with a 2048-byte body
  /?token=1  - 200 OK (per-signal endpoint with a query and no path)
  /header/<name>/<value> - 200 OK if the request header <name> equals <value>, else 400
"""
import gzip
import http.server
import json
import sys
import time

retry_counts = {}

WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
WEEKDAYS_FULL = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def http_date(timestamp, date_format):
    t = time.gmtime(timestamp)
    clock = f'{t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}'
    month = MONTHS[t.tm_mon - 1]
    if date_format == 'rfc850':
        return f'{WEEKDAYS_FULL[t.tm_wday]}, {t.tm_mday:02d}-{month}-{t.tm_year % 100:02d} {clock} GMT'
    if date_format == 'asctime':
        return f'{WEEKDAYS[t.tm_wday]} {month} {t.tm_mday:2d} {clock} {t.tm_year}'
    return f'{WEEKDAYS[t.tm_wday]}, {t.tm_mday:02d} {month} {t.tm_year} {clock} GMT'


class OTLPMockHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b''

        if self.path in ('/v1/traces', '/v1/logs', '/v1/metrics'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{}')
        elif self.path == '/v1/gzip-traces':
            encoding = self.headers.get('Content-Encoding', '')
            if encoding != 'gzip':
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'missing Content-Encoding: gzip')
                return
            try:
                decompressed = gzip.decompress(body)
                data = json.loads(decompressed)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"decompressedSize": len(decompressed)}).encode())
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(f'invalid gzip: {e}'.encode())
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
        elif self.path.startswith('/retry-after/'):
            self.send_response(429)
            self.send_header('Retry-After', self.path.split('/')[2])
            self.end_headers()
            self.wfile.write(b'too many requests')
        elif self.path.startswith('/retry-after-date/'):
            _, _, date_format, seconds = self.path.split('/')
            self.send_response(429)
            self.send_header('Retry-After', http_date(time.time() + int(seconds), date_format))
            self.end_headers()
            self.wfile.write(b'too many requests')
        elif self.path == '/big-response':
            body = b'{"partialSuccess":{"errorMessage":"' + b'x' * 2000 + b'"}}'
            body = body + b' ' * (2048 - len(body))
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == '/?token=1':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{}')
        elif self.path.startswith('/header/'):
            _, _, name, value = self.path.split('/', 3)
            actual = self.headers.get(name)
            if actual == value:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{}')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(f'header {name}: {actual}'.encode())
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
