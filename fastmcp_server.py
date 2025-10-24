#!/usr/bin/env python3
"""
SF Parking MCP Server using FastMCP
Provides access to San Francisco parking data via ArcGIS REST API
"""

import json
import urllib.parse
from typing import Optional
import httpx
from fastmcp import FastMCP

# Base URL for the ArcGIS REST API
BASE_URL = "https://services.sfmta.com/arcgis/rest/services/Parking/sfpark_ODS/MapServer/4/query"

# Create FastMCP server
mcp = FastMCP("SF Parking")


def build_query_url(
    geometry: Optional[dict] = None,
    where: str = "1=1",
    out_fields: str = "*",
    max_records: int = 1000,
) -> str:
    """Build ArcGIS REST API query URL with parameters"""
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


async def query_parking_api(url: str) -> dict:
    """Make async request to parking API"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_parking_by_bbox(
    min_lat: float,
    min_lon: float,
    max_lat: float,
    max_lon: float,
    max_records: int = 100
) -> str:
    """
    Get parking blockface data within a bounding box (lat/lon coordinates).

    Returns street parking availability, rates, and location information for SF parking zones.

    Args:
        min_lat: Minimum latitude (south boundary)
        min_lon: Minimum longitude (west boundary)
        max_lat: Maximum latitude (north boundary)
        max_lon: Maximum longitude (east boundary)
        max_records: Maximum number of records to return (default: 100, max: 1000)

    Returns:
        JSON string with parking data
    """
    geometry = {
        "xmin": min_lon,
        "ymin": min_lat,
        "xmax": max_lon,
        "ymax": max_lat,
    }

    url = build_query_url(
        geometry=geometry,
        max_records=min(max_records, 1000)
    )

    data = await query_parking_api(url)
    return json.dumps(data, indent=2)


@mcp.tool()
async def get_parking_by_street(
    street_name: str,
    max_records: int = 50
) -> str:
    """
    Search for parking blockface data by street name.

    Returns availability, rates, and location information for matching streets in San Francisco.

    Args:
        street_name: Street name to search for (e.g., 'Market', 'Mission')
        max_records: Maximum number of records to return (default: 50, max: 1000)

    Returns:
        JSON string with parking data
    """
    where = f"STREET_NAME LIKE '%{street_name.upper()}%'"

    url = build_query_url(
        where=where,
        max_records=min(max_records, 1000)
    )

    data = await query_parking_api(url)
    return json.dumps(data, indent=2)


@mcp.tool()
async def get_parking_by_location(
    latitude: float,
    longitude: float,
    max_records: int = 20
) -> str:
    """
    Get parking blockface data near a specific point (lat/lon).

    Searches within approximately 200 meters of the given coordinates.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
        max_records: Maximum number of records to return (default: 20, max: 1000)

    Returns:
        JSON string with parking data
    """
    offset = 0.0018  # Approximately 200 meters at SF latitude
    geometry = {
        "xmin": longitude - offset,
        "ymin": latitude - offset,
        "xmax": longitude + offset,
        "ymax": latitude + offset,
    }

    url = build_query_url(
        geometry=geometry,
        max_records=min(max_records, 1000)
    )

    data = await query_parking_api(url)
    return json.dumps(data, indent=2)


if __name__ == "__main__":
    # Run with HTTP transport for cloud deployment
    # Or use default stdio for local/Claude Desktop
    import sys

    if "--http" in sys.argv:
        mcp.run(transport="http", host="0.0.0.0", port=8000)
    else:
        mcp.run()
