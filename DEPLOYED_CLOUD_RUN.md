# 🎉 Your MCP Server is LIVE on Google Cloud Run!

## Deployment Success!

Your SF Parking MCP server is now running at:

**https://sf-parking-mcp-586287909845.us-central1.run.app**

## Use with Claude Desktop

Add this to your Claude Desktop config:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "sf-parking-cloud": {
      "url": "https://sf-parking-mcp-586287909845.us-central1.run.app/mcp"
    }
  }
}
```

**Restart Claude Desktop** and you'll see your 3 parking tools available!

## Test It

Ask Claude:
- "What's the parking situation near Union Square in SF?"
- "Find parking on Market Street"
- "Show me parking rates downtown San Francisco"

Claude will call YOUR hosted MCP server and get real parking data!

## What You Got

✅ **Free hosting** on Google Cloud Run
✅ **2 million requests/month FREE**
✅ **Auto-scaling** - scales to zero when not in use (no cost!)
✅ **Global CDN** with HTTPS
✅ **3 MCP tools** for SF parking data
✅ **Always available** - no "server sleeping"

## Manage Your Deployment

### View logs:
```bash
gcloud run logs read sf-parking-mcp --region us-central1
```

### Redeploy after changes:
```bash
gcloud run deploy sf-parking-mcp \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000
```

### Delete the service (if needed):
```bash
gcloud run services delete sf-parking-mcp --region us-central1
```

## Cost

**FREE** within these limits (per month):
- 2 million requests
- 360,000 GB-seconds of memory
- 180,000 vCPU-seconds

Your MCP server will stay well within these limits!

## Dashboard

View your deployment:
https://console.cloud.google.com/run?project=sf-parking-mcp

## Files

- `fastmcp_server.py` - FastMCP server with 3 tools
- `Dockerfile` - Container configuration
- `pyproject.toml` - Python dependencies

## Available Tools

1. **get_parking_by_bbox** - Query parking in a lat/lon bounding box
2. **get_parking_by_street** - Search for parking by street name
3. **get_parking_by_location** - Find parking near specific coordinates

All tools return real-time SF parking data including rates, availability, and schedules!

---

**Your MCP server is live and ready to use!** 🚗🅿️
