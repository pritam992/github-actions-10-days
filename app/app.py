import json
from http.server import BaseHTTPRequestHandler, HTTPServer


def response(path):
    if path == '/health':
        return 200, {'status': 'ok'}
    if path == '/':
        return 200, {'message': 'Ship small. Learn daily.'}
    return 404, {'error': 'not found'}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, body = response(self.path)
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == '__main__':
    HTTPServer(('0.0.0.0', 8000), Handler).serve_forever()
