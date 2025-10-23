#!/usr/bin/env python3
"""
SF Parking MCP Server
Provides access to San Francisco parking data via ArcGIS REST API
"""

import asyncio
import json
import urllib.parse
from typing import Any, Optional
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

# Base URL for the ArcGIS REST API
BASE_URL = "https://services.sfmta.com/arcgis/rest/services/Parking/sfpark_ODS/MapServer/4/query"

app = Server("sf-parking")


def build_query_url(
    geometry: Optional[dict] = None,
    where: str = "1=1",
    out_fields: str = "*",
    return_geometry: bool = True,
    max_records: int = 1000,
) -> str:
    """Build ArcGIS REST API query URL with parameters"""

    params = {
        "f": "json",
        "where": where,
        "outFields": out_fields,
        "returnGeometry": "true" if return_geometry else "false",
        "outSR": "4326",  # WGS84 lat/lon
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


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools"""
    return [
        Tool(
            name="get_parking_by_bbox",
            description="Get parking blockface data within a bounding box (lat/lon coordinates). Returns street parking availability, rates, and location information for SF parking zones.",
            inputSchema={
                "type": "object",
                "properties": {
                    "min_lat": {
                        "type": "number",
                        "description": "Minimum latitude (south boundary)",
                    },
                    "min_lon": {
                        "type": "number",
                        "description": "Minimum longitude (west boundary)",
                    },
                    "max_lat": {
                        "type": "number",
                        "description": "Maximum latitude (north boundary)",
                    },
                    "max_lon": {
                        "type": "number",
                        "description": "Maximum longitude (east boundary)",
                    },
                    "max_records": {
                        "type": "number",
                        "description": "Maximum number of records to return (default: 100, max: 1000)",
                        "default": 100,
                    },
                },
                "required": ["min_lat", "min_lon", "max_lat", "max_lon"],
            },
        ),
        Tool(
            name="get_parking_by_street",
            description="Search for parking blockface data by street name. Returns availability, rates, and location information for matching streets in San Francisco.",
            inputSchema={
                "type": "object",
                "properties": {
                    "street_name": {
                        "type": "string",
                        "description": "Street name to search for (e.g., 'Market', 'Mission')",
                    },
                    "max_records": {
                        "type": "number",
                        "description": "Maximum number of records to return (default: 50, max: 1000)",
                        "default": 50,
                    },
                },
                "required": ["street_name"],
            },
        ),
        Tool(
            name="get_parking_by_location",
            description="Get parking blockface data near a specific point (lat/lon). Searches within approximately 200 meters of the given coordinates.",
            inputSchema={
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "Latitude of the location",
                    },
                    "longitude": {
                        "type": "number",
                        "description": "Longitude of the location",
                    },
                    "max_records": {
                        "type": "number",
                        "description": "Maximum number of records to return (default: 20, max: 1000)",
                        "default": 20,
                    },
                },
                "required": ["latitude", "longitude"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""

    try:
        if name == "get_parking_by_bbox":
            # Build bounding box geometry
            geometry = {
                "xmin": arguments["min_lon"],
                "ymin": arguments["min_lat"],
                "xmax": arguments["max_lon"],
                "ymax": arguments["max_lat"],
            }
            max_records = arguments.get("max_records", 100)

            url = build_query_url(
                geometry=geometry,
                max_records=min(max_records, 1000)
            )

            data = await query_parking_api(url)

            return [
                TextContent(
                    type="text",
                    text=json.dumps(data, indent=2),
                )
            ]

        elif name == "get_parking_by_street":
            street_name = arguments["street_name"]
            max_records = arguments.get("max_records", 50)

            # Build SQL WHERE clause for street search
            where = f"STREET_NAME LIKE '%{street_name.upper()}%'"

            url = build_query_url(
                where=where,
                max_records=min(max_records, 1000)
            )

            data = await query_parking_api(url)

            return [
                TextContent(
                    type="text",
                    text=json.dumps(data, indent=2),
                )
            ]

        elif name == "get_parking_by_location":
            lat = arguments["latitude"]
            lon = arguments["longitude"]
            max_records = arguments.get("max_records", 20)

            # Create a small bounding box around the point (~200m)
            offset = 0.0018  # Approximately 200 meters at SF latitude
            geometry = {
                "xmin": lon - offset,
                "ymin": lat - offset,
                "xmax": lon + offset,
                "ymax": lat + offset,
            }

            url = build_query_url(
                geometry=geometry,
                max_records=min(max_records, 1000)
            )

            data = await query_parking_api(url)

            return [
                TextContent(
                    type="text",
                    text=json.dumps(data, indent=2),
                )
            ]

        else:
            return [
                TextContent(
                    type="text",
                    text=f"Unknown tool: {name}",
                )
            ]

    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"Error: {str(e)}",
            )
        ]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
