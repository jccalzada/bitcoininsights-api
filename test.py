from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "message": "CoinGlass API Gateway is working on Vercel!",
            "status": "success",
            "timestamp": "2025-07-15T00:00:00Z"
        }
        
        self.wfile.write(json.dumps(response).encode())
        return

