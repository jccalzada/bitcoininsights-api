from http.server import BaseHTTPRequestHandler
import json
import requests
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        exchange = query_params.get('exchange', ['binance'])[0]
        
        try:
            # CoinGlass API call
            url = "https://open-api-v4.coinglass.com/api/futures/global-long-short-account-ratio/history"
            params = {
                'symbol': 'BTC',
                'exchange': exchange,
                'interval': '1d',
                'limit': 1
            }
            headers = {
                'CG-API-KEY': '8dde1df481bd440eb6fe0e97bf856fcc'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('code') == "0" and data.get('data'):
                    latest = data['data'][0]
                    result = {
                        "code": "0",
                        "data": {
                            "global_account_long_percent": latest['longAccount'] * 100,
                            "global_account_short_percent": latest['shortAccount'] * 100,
                            "global_account_long_short_ratio": latest['longShortRatio']
                        },
                        "source": "coinglass_api",
                        "status": "success"
                    }
                else:
                    raise Exception("Invalid API response")
            else:
                raise Exception(f"API error: {response.status_code}")
                
        except Exception as e:
            # Fallback data
            fallback_data = {
                'binance': {'long': 36.57, 'short': 63.43},
                'bybit': {'long': 34.2, 'short': 65.8},
                'okx': {'long': 38.1, 'short': 61.9},
                'bitget': {'long': 35.8, 'short': 64.2}
            }
            
            data = fallback_data.get(exchange, fallback_data['binance'])
            result = {
                "code": "0",
                "data": {
                    "global_account_long_percent": data['long'],
                    "global_account_short_percent": data['short'],
                    "global_account_long_short_ratio": data['long'] / data['short']
                },
                "source": "fallback",
                "status": "success"
            }
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
        return

