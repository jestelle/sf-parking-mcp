# Using SF Parking API with Claude Desktop

Your SF Parking API is deployed and you can use it with Claude in two ways:

## Option 1: Use REST API with Web Fetch (Works Now!)

Claude can fetch parking data directly from your REST API using web requests.

Just ask Claude questions like:

- "Fetch parking data from https://sf-parking.vercel.app/api?tool=location&lat=37.7833&lon=-122.4167 and summarize the parking options"
- "Get parking on Market Street using https://sf-parking.vercel.app/api?tool=street&name=Market and tell me the rates"
- "Check parking availability in the financial district using https://sf-parking.vercel.app/api?tool=bbox&min_lat=37.79&min_lon=-122.41&max_lat=37.80&max_lon=-122.39"

Claude will fetch the data and interpret it for you!

## Option 2: MCP Server (Future)

For native MCP support, you'll need an SSE endpoint. The REST API works great for now, and you can add proper MCP SSE transport later if needed.

An MCP endpoint would allow Claude Desktop to list the tools natively, but the REST API approach works just as well for querying parking data.

## Example Conversation

**You:** "What's the parking situation near Union Square in SF?"

**Claude:** *[Fetches from your API]* "Let me check the parking data for that area..."

```
curl "https://sf-parking.vercel.app/api?tool=bbox&min_lat=37.787&min_lon=-122.408&max_lat=37.790&max_lon=-122.405"
```

*[Interprets the results]* "There are several metered parking options near Union Square. Rates range from $3.50-$5.75 per hour..."

## API Endpoints Reference

- **Location**: `/api?tool=location&lat={lat}&lon={lon}`
- **Street**: `/api?tool=street&name={street}`
- **Bounding Box**: `/api?tool=bbox&min_lat={lat1}&min_lon={lon1}&max_lat={lat2}&max_lon={lon2}`

All endpoints return JSON with parking data including rates, schedules, and availability.

## Your Deployed API

**Base URL:** https://sf-parking.vercel.app/api

**Status:** ✅ Live and working
**Cost:** FREE on Vercel
**Updates:** Auto-deploy from GitHub

Enjoy! 🚗🅿️
