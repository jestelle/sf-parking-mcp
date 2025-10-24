/**
 * SF Parking MCP Server - SSE Transport
 * Provides MCP protocol access to San Francisco parking data
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const BASE_URL = "https://services.sfmta.com/arcgis/rest/services/Parking/sfpark_ODS/MapServer/4/query";

/**
 * Query the parking API
 */
async function queryParkingAPI(params) {
  const queryParams = new URLSearchParams({
    f: "json",
    outFields: "*",
    returnGeometry: "false",
    outSR: "4326",
    ...params
  });

  const url = `${BASE_URL}?${queryParams.toString()}`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`ArcGIS API error: ${response.status}`);
  }

  return await response.json();
}

/**
 * Create and configure the MCP server
 */
function createServer() {
  const server = new Server(
    {
      name: "sf-parking",
      version: "0.1.0",
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );

  // List available tools
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: [
        {
          name: "get_parking_by_bbox",
          description: "Get parking blockface data within a bounding box (lat/lon coordinates). Returns street parking availability, rates, and location information for SF parking zones.",
          inputSchema: {
            type: "object",
            properties: {
              min_lat: {
                type: "number",
                description: "Minimum latitude (south boundary)",
              },
              min_lon: {
                type: "number",
                description: "Minimum longitude (west boundary)",
              },
              max_lat: {
                type: "number",
                description: "Maximum latitude (north boundary)",
              },
              max_lon: {
                type: "number",
                description: "Maximum longitude (east boundary)",
              },
              max_records: {
                type: "number",
                description: "Maximum number of records to return (default: 100, max: 1000)",
                default: 100,
              },
            },
            required: ["min_lat", "min_lon", "max_lat", "max_lon"],
          },
        },
        {
          name: "get_parking_by_street",
          description: "Search for parking blockface data by street name. Returns availability, rates, and location information for matching streets in San Francisco.",
          inputSchema: {
            type: "object",
            properties: {
              street_name: {
                type: "string",
                description: "Street name to search for (e.g., 'Market', 'Mission')",
              },
              max_records: {
                type: "number",
                description: "Maximum number of records to return (default: 50, max: 1000)",
                default: 50,
              },
            },
            required: ["street_name"],
          },
        },
        {
          name: "get_parking_by_location",
          description: "Get parking blockface data near a specific point (lat/lon). Searches within approximately 200 meters of the given coordinates.",
          inputSchema: {
            type: "object",
            properties: {
              latitude: {
                type: "number",
                description: "Latitude of the location",
              },
              longitude: {
                type: "number",
                description: "Longitude of the location",
              },
              max_records: {
                type: "number",
                description: "Maximum number of records to return (default: 20, max: 1000)",
                default: 20,
              },
            },
            required: ["latitude", "longitude"],
          },
        },
      ],
    };
  });

  // Handle tool calls
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    try {
      let queryParams = {};
      let data;

      switch (name) {
        case "get_parking_by_bbox": {
          const geometry = JSON.stringify({
            xmin: args.min_lon,
            ymin: args.min_lat,
            xmax: args.max_lon,
            ymax: args.max_lat,
          });

          queryParams = {
            where: "1=1",
            geometry,
            geometryType: "esriGeometryEnvelope",
            spatialRel: "esriSpatialRelIntersects",
            inSR: "4326",
            resultRecordCount: String(Math.min(args.max_records || 100, 1000)),
          };

          data = await queryParkingAPI(queryParams);
          break;
        }

        case "get_parking_by_street": {
          queryParams = {
            where: `STREET_NAME LIKE '%${args.street_name.toUpperCase()}%'`,
            resultRecordCount: String(Math.min(args.max_records || 50, 1000)),
          };

          data = await queryParkingAPI(queryParams);
          break;
        }

        case "get_parking_by_location": {
          const offset = 0.0018; // ~200 meters
          const geometry = JSON.stringify({
            xmin: args.longitude - offset,
            ymin: args.latitude - offset,
            xmax: args.longitude + offset,
            ymax: args.latitude + offset,
          });

          queryParams = {
            where: "1=1",
            geometry,
            geometryType: "esriGeometryEnvelope",
            spatialRel: "esriSpatialRelIntersects",
            inSR: "4326",
            resultRecordCount: String(Math.min(args.max_records || 20, 1000)),
          };

          data = await queryParkingAPI(queryParams);
          break;
        }

        default:
          throw new Error(`Unknown tool: ${name}`);
      }

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(data, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error: ${error.message}`,
          },
        ],
        isError: true,
      };
    }
  });

  return server;
}

/**
 * Vercel serverless handler for MCP over SSE
 */
export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const server = createServer();
  const transport = new SSEServerTransport("/api/sse", res);

  await server.connect(transport);

  // Keep connection alive for SSE
  req.on('close', () => {
    server.close();
  });
}
