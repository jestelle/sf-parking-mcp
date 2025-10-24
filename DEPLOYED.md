# 🎉 SF Parking API - DEPLOYED!

Your San Francisco parking API is now **live and working** at:

**https://sf-parking.vercel.app/api**

## Quick Test

Try it now:
```bash
curl "https://sf-parking.vercel.app/api?tool=location&lat=37.7833&lon=-122.4167"
```

## API Endpoints

### 1. Get Parking by Location
Find parking near a specific point:
```
https://sf-parking.vercel.app/api?tool=location&lat=37.7833&lon=-122.4167
```

**Parameters:**
- `tool=location`
- `lat` - Latitude
- `lon` - Longitude

**Returns:** Parking within ~200 meters

### 2. Get Parking by Bounding Box
Get all parking in an area:
```
https://sf-parking.vercel.app/api?tool=bbox&min_lat=37.77&min_lon=-122.42&max_lat=37.78&max_lon=-122.41
```

**Parameters:**
- `tool=bbox`
- `min_lat`, `min_lon` - Southwest corner
- `max_lat`, `max_lon` - Northeast corner

**Returns:** Up to 100 parking spots in the area

### 3. Search by Street Name
Find parking on a specific street:
```
https://sf-parking.vercel.app/api?tool=street&name=Market
```

**Parameters:**
- `tool=street`
- `name` - Street name to search

**Returns:** Up to 50 matching parking spots

## Response Format

Each parking spot includes:
```json
{
  "STREET_NAME": "Eddy St",
  "ADDR_RANGE": "401-499",
  "LATITUDE": 37.7833,
  "LONGITUDE": -122.4167,
  "RATE": "$3.50 per hour",
  "RATE_SCHED": "<html>...full schedule...</html>",
  "AVAIL_MSG": "Availability message",
  "AVAIL_THRESHOLD": 4.0
}
```

## Use with Claude Desktop

While this is a REST API (not a traditional MCP server), you can still use it with Claude by having Claude fetch from these URLs.

Just ask Claude:
> "Fetch parking data from https://sf-parking.vercel.app/api?tool=location&lat=37.7833&lon=-122.4167 and tell me about parking options"

## Cost

**FREE** on Vercel:
- ✓ Unlimited requests
- ✓ Global CDN
- ✓ Auto-scaling
- ✓ HTTPS included
- ✓ No credit card required

## Update the API

```bash
cd /Users/joshestelle/tools/sf-parking
# Make changes to api/index.js
git add .
git commit -m "Update API"
git push
# Vercel auto-deploys in ~30 seconds
```

## Examples

### Find parking downtown
```bash
curl "https://sf-parking.vercel.app/api?tool=bbox&min_lat=37.78&min_lon=-122.42&max_lat=37.79&max_lon=-122.40"
```

### Check parking on your street
```bash
curl "https://sf-parking.vercel.app/api?tool=street&name=Mission"
```

### Parking near coordinates
```bash
curl "https://sf-parking.vercel.app/api?tool=location&lat=37.7749&lon=-122.4194"
```

## What You Got

1. **Live API** - Working REST API on Vercel
2. **Real SF Parking Data** - From SFMTA ArcGIS
3. **Free hosting** - Forever on Vercel
4. **Auto-deploy** - Push to GitHub, auto-updates
5. **Global CDN** - Fast from anywhere

Enjoy your deployed parking API! 🚗🅿️
