/**
 * SF Parking MCP Server using mcp-handler
 * CommonJS version for Vercel compatibility
 */

const { createMCPHandler } = require("mcp-handler");

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
 * Define MCP tools
 */
const tools = [
  {
    name: "get_parking_by_bbox",
    description: "Get parking blockface data within a bounding box (lat/lon coordinates). Returns street parking availability, rates, and location information for SF parking zones.",
    parameters: {
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
    handler: async (params) => {
      const geometry = JSON.stringify({
        xmin: params.min_lon,
        ymin: params.min_lat,
        xmax: params.max_lon,
        ymax: params.max_lat,
      });

      const queryParams = {
        where: "1=1",
        geometry,
        geometryType: "esriGeometryEnvelope",
        spatialRel: "esriSpatialRelIntersects",
        inSR: "4326",
        resultRecordCount: String(Math.min(params.max_records || 100, 1000)),
      };

      const data = await queryParkingAPI(queryParams);
      return JSON.stringify(data, null, 2);
    },
  },
  {
    name: "get_parking_by_street",
    description: "Search for parking blockface data by street name. Returns availability, rates, and location information for matching streets in San Francisco.",
    parameters: {
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
    handler: async (params) => {
      const queryParams = {
        where: `STREET_NAME LIKE '%${params.street_name.toUpperCase()}%'`,
        resultRecordCount: String(Math.min(params.max_records || 50, 1000)),
      };

      const data = await queryParkingAPI(queryParams);
      return JSON.stringify(data, null, 2);
    },
  },
  {
    name: "get_parking_by_location",
    description: "Get parking blockface data near a specific point (lat/lon). Searches within approximately 200 meters of the given coordinates.",
    parameters: {
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
    handler: async (params) => {
      const offset = 0.0018; // ~200 meters
      const geometry = JSON.stringify({
        xmin: params.longitude - offset,
        ymin: params.latitude - offset,
        xmax: params.longitude + offset,
        ymax: params.latitude + offset,
      });

      const queryParams = {
        where: "1=1",
        geometry,
        geometryType: "esriGeometryEnvelope",
        spatialRel: "esriSpatialRelIntersects",
        inSR: "4326",
        resultRecordCount: String(Math.min(params.max_records || 20, 1000)),
      };

      const data = await queryParkingAPI(queryParams);
      return JSON.stringify(data, null, 2);
    },
  },
];

/**
 * Create and export MCP handler for Vercel
 */
module.exports = createMCPHandler({
  name: "sf-parking",
  version: "0.1.0",
  tools,
});
