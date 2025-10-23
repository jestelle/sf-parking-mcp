#!/usr/bin/env python3
"""Quick test to verify the SF Parking API is accessible"""

import asyncio
import httpx
import json

async def test_api():
    """Test the parking API endpoint"""

    # Test query for any data
    url = "https://services.sfmta.com/arcgis/rest/services/Parking/sfpark_ODS/MapServer/4/query"
    params = {
        "f": "json",
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "false",
        "resultRecordCount": "5",
    }

    print("Testing SF Parking API...")
    print(f"Query: {params['where']} (get any records)\n")

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if "features" in data and len(data["features"]) > 0:
            print(f"✓ Success! Found {len(data['features'])} results")
            print("\nSample result:")
            if "attributes" in data["features"][0]:
                attrs = data["features"][0]["attributes"]
                print(json.dumps(attrs, indent=2))
        else:
            print("✗ No results found")
            print(json.dumps(data, indent=2))

if __name__ == "__main__":
    asyncio.run(test_api())
