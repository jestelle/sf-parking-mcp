import json
import urllib.request
import urllib.parse
from urllib.parse import urlparse, parse_qs

BASE_URL = "https://services.sfmta.com/arcgis/rest/services/Parking/sfpark_ODS/MapServer/4/query"


def handler(request):
    """Vercel serverless function handler"""

    # Parse the request
    parsed = urlparse(request.url)
    path = parsed.path
    params = parse_qs(parsed.query)

    # CORS headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

    # Handle OPTIONS for CORS
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }

    # Root endpoint
    if not params.get('tool'):
        info = {
            "name": "sf-parking",
            "version": "0.1.0",
            "description": "SF Parking API - San Francisco parking data",
            "tools": [
                "bbox - Get parking in bounding box",
                "street - Search by street name",
                "location - Find near a point"
            ],
            "examples": {
                "bbox": "?tool=bbox&min_lat=37.77&min_lon=-122.42&max_lat=37.78&max_lon=-122.41",
                "street": "?tool=street&name=Market",
                "location": "?tool=location&lat=37.7833&lon=-122.4167"
            }
        }
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(info, indent=2)
        }

    # Get tool type
    tool = params.get('tool', [None])[0]

    try:
        # Build API URL based on tool
        if tool == 'bbox':
            min_lat = float(params.get('min_lat', [0])[0])
            min_lon = float(params.get('min_lon', [0])[0])
            max_lat = float(params.get('max_lat', [0])[0])
            max_lon = float(params.get('max_lon', [0])[0])

            api_params = {
                "f": "json",
                "where": "1=1",
                "outFields": "*",
                "returnGeometry": "false",
                "outSR": "4326",
                "resultRecordCount": "100",
                "geometry": json.dumps({
                    "xmin": min_lon, "ymin": min_lat,
                    "xmax": max_lon, "ymax": max_lat
                }),
                "geometryType": "esriGeometryEnvelope",
                "spatialRel": "esriSpatialRelIntersects",
                "inSR": "4326"
            }

        elif tool == 'street':
            name = params.get('name', [''])[0]
            api_params = {
                "f": "json",
                "where": f"STREET_NAME LIKE '%{name.upper()}%'",
                "outFields": "*",
                "returnGeometry": "false",
                "outSR": "4326",
                "resultRecordCount": "50"
            }

        elif tool == 'location':
            lat = float(params.get('lat', [0])[0])
            lon = float(params.get('lon', [0])[0])
            offset = 0.0018

            api_params = {
                "f": "json",
                "where": "1=1",
                "outFields": "*",
                "returnGeometry": "false",
                "outSR": "4326",
                "resultRecordCount": "20",
                "geometry": json.dumps({
                    "xmin": lon - offset, "ymin": lat - offset,
                    "xmax": lon + offset, "ymax": lat + offset
                }),
                "geometryType": "esriGeometryEnvelope",
                "spatialRel": "esriSpatialRelIntersects",
                "inSR": "4326"
            }
        else:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({"error": f"Invalid tool: {tool}"})
            }

        # Make request to ArcGIS API
        url = f"{BASE_URL}?{urllib.parse.urlencode(api_params)}"
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(data, indent=2)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({"error": str(e)})
        }
