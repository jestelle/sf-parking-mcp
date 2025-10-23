/**
 * SF Parking API - Vercel Serverless Function
 * Provides access to San Francisco parking data via ArcGIS REST API
 */

const BASE_URL = "https://services.sfmta.com/arcgis/rest/services/Parking/sfpark_ODS/MapServer/4/query";

/**
 * Build ArcGIS query URL
 */
function buildQueryUrl(params) {
  const queryParams = new URLSearchParams({
    f: "json",
    outFields: "*",
    returnGeometry: "false",
    outSR: "4326",
    ...params
  });

  return `${BASE_URL}?${queryParams.toString()}`;
}

/**
 * Main handler function
 */
export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle OPTIONS for CORS preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const { tool, min_lat, min_lon, max_lat, max_lon, name, lat, lon } = req.query;

  // Root endpoint - show API info
  if (!tool) {
    return res.status(200).json({
      name: "sf-parking-api",
      version: "0.1.0",
      description: "San Francisco parking data API",
      tools: {
        bbox: "Get parking in a bounding box",
        street: "Search by street name",
        location: "Find parking near coordinates"
      },
      examples: {
        bbox: "/api?tool=bbox&min_lat=37.77&min_lon=-122.42&max_lat=37.78&max_lon=-122.41",
        street: "/api?tool=street&name=Market",
        location: "/api?tool=location&lat=37.7833&lon=-122.4167"
      }
    });
  }

  try {
    let queryParams = {};

    // Handle different tool types
    if (tool === 'bbox') {
      if (!min_lat || !min_lon || !max_lat || !max_lon) {
        return res.status(400).json({
          error: "Missing required parameters: min_lat, min_lon, max_lat, max_lon"
        });
      }

      const geometry = JSON.stringify({
        xmin: parseFloat(min_lon),
        ymin: parseFloat(min_lat),
        xmax: parseFloat(max_lon),
        ymax: parseFloat(max_lat)
      });

      queryParams = {
        where: "1=1",
        geometry,
        geometryType: "esriGeometryEnvelope",
        spatialRel: "esriSpatialRelIntersects",
        inSR: "4326",
        resultRecordCount: "100"
      };

    } else if (tool === 'street') {
      if (!name) {
        return res.status(400).json({
          error: "Missing required parameter: name"
        });
      }

      queryParams = {
        where: `STREET_NAME LIKE '%${name.toUpperCase()}%'`,
        resultRecordCount: "50"
      };

    } else if (tool === 'location') {
      if (!lat || !lon) {
        return res.status(400).json({
          error: "Missing required parameters: lat, lon"
        });
      }

      const latitude = parseFloat(lat);
      const longitude = parseFloat(lon);
      const offset = 0.0018; // ~200 meters

      const geometry = JSON.stringify({
        xmin: longitude - offset,
        ymin: latitude - offset,
        xmax: longitude + offset,
        ymax: latitude + offset
      });

      queryParams = {
        where: "1=1",
        geometry,
        geometryType: "esriGeometryEnvelope",
        spatialRel: "esriSpatialRelIntersects",
        inSR: "4326",
        resultRecordCount: "20"
      };

    } else {
      return res.status(400).json({
        error: `Invalid tool: ${tool}. Use: bbox, street, or location`
      });
    }

    // Fetch data from ArcGIS API
    const url = buildQueryUrl(queryParams);
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`ArcGIS API error: ${response.status}`);
    }

    const data = await response.json();
    return res.status(200).json(data);

  } catch (error) {
    console.error('API Error:', error);
    return res.status(500).json({
      error: error.message || 'Internal server error'
    });
  }
}
