from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
from urllib.parse import urlparse, parse_qs
import httpx


BASE_URL = "https://services.sfmta.com/arcgis/rest/services/Parking/sfpark_ODS/MapServer/4/query"


def build_query_url(geometry=None, where="1=1", out_fields="*", max_records=1000):
    """Build ArcGIS REST API query URL"""
    params = {
        "f": "json",
        "where": where,
        "outFields": out_fields,
        "returnGeometry": "false",
        "outSR": "4326",
        "resultRecordCount": str(max_records),
    }

    if geometry:
        params["geometry"] = json.dumps(geometry)
        params["geometryType"] = "esriGeometryEnvelope"
        params["spatialRel"] = "esriSpatialRelIntersects"
        params["inSR"] = "4326"

    return f"{BASE_URL}?{urllib.parse.urlencode(params)}"


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        # Root endpoint - return MCP server info
        if path == "/" or path == "/mcp":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response = {
                "name": "sf-parking",
                "version": "0.1.0",
                "description": "SF Parking MCP Server - Access San Francisco parking data",
                "tools": [
                    {
                        "name": "get_parking_by_bbox",
                        "description": "Get parking data within a bounding box",
                        "parameters": {
                            "min_lat": "number",
                            "min_lon": "number",
                            "max_lat": "number",
                            "max_lon": "number"
                        }
                    },
                    {
                        "name": "get_parking_by_street",
                        "description": "Search parking by street name",
                        "parameters": {
                            "street_name": "string"
                        }
                    },
                    {
                        "name": "get_parking_by_location",
                        "description": "Find parking near a point",
                        "parameters": {
                            "latitude": "number",
                            "longitude": "number"
                        }
                    }
                ],
                "endpoints": {
                    "bbox": "/api/mcp?tool=bbox&min_lat=37.77&min_lon=-122.42&max_lat=37.78&max_lon=-122.41",
                    "street": "/api/mcp?tool=street&name=Market",
                    "location": "/api/mcp?tool=location&lat=37.7833&lon=-122.4167"
                }
            }

            self.wfile.write(json.dumps(response, indent=2).encode())
            return

        # Handle tool requests
        tool = params.get('tool', [None])[0]

        try:
            if tool == 'bbox':
                min_lat = float(params.get('min_lat', [0])[0])
                min_lon = float(params.get('min_lon', [0])[0])
                max_lat = float(params.get('max_lat', [0])[0])
                max_lon = float(params.get('max_lon', [0])[0])

                geometry = {
                    "xmin": min_lon,
                    "ymin": min_lat,
                    "xmax": max_lon,
                    "ymax": max_lat
                }
                url = build_query_url(geometry=geometry)

            elif tool == 'street':
                name = params.get('name', [''])[0]
                where = f"STREET_NAME LIKE '%{name.upper()}%'"
                url = build_query_url(where=where, max_records=50)

            elif tool == 'location':
                lat = float(params.get('lat', [0])[0])
                lon = float(params.get('lon', [0])[0])
                offset = 0.0018

                geometry = {
                    "xmin": lon - offset,
                    "ymin": lat - offset,
                    "xmax": lon + offset,
                    "ymax": lat + offset
                }
                url = build_query_url(geometry=geometry, max_records=20)

            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid tool. Use: bbox, street, or location"}).encode())
                return

            # Fetch data from API
            with httpx.Client(timeout=30.0) as client:
                response = client.get(url)
                response.raise_for_status()
                data = response.json()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data, indent=2).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
