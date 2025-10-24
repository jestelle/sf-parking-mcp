# SF Parking API

A REST API that provides access to San Francisco parking data via the SFMTA ArcGIS REST API.

**🎉 Live API:** https://sf-parking.vercel.app/api

## Features

This server exposes three tools for querying SF parking blockface data:

- **get_parking_by_bbox**: Query parking data within a bounding box (lat/lon coordinates)
- **get_parking_by_street**: Search for parking by street name
- **get_parking_by_location**: Find parking near a specific point

Data includes street parking availability, rates, schedules, and location information for all SF parking zones.

## Installation

### Option 1: Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone or download this repository
git clone <your-repo-url>
cd sf-parking

# Install dependencies
uv sync
```

### Option 2: Using pip

```bash
pip install -e .
```

### Option 3: Install from PyPI (after publishing)

```bash
pip install sf-parking-mcp
```

## Usage

### With Claude Desktop

Add this to your Claude Desktop configuration file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "sf-parking": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/sf-parking",
        "run",
        "server.py"
      ]
    }
  }
}
```

Or if installed via pip:

```json
{
  "mcpServers": {
    "sf-parking": {
      "command": "python",
      "args": ["-m", "server"]
    }
  }
}
```

### Standalone Testing

```bash
# Run the server directly
uv run server.py
```

## Example Queries

Once connected, you can ask Claude questions like:

- "What's the parking availability on Market Street?"
- "Find parking near coordinates 37.7749, -122.4194"
- "Show me all parking in the area bounded by 37.77, -122.42 and 37.78, -122.41"

## API Details

This server queries the SFMTA ArcGIS REST API:
- **Endpoint**: `sfpark_ODS.BLOCKFACE_RATES_VW`
- **Data**: Real-time parking blockface rates, availability, and location info
- **Max records per query**: 1000

### Available Fields

- Location: Street name, address range, lat/lon, orientation
- Availability: Threshold values, availability messages
- Pricing: Rate details, schedules, thresholds
- Identifiers: Blockface ID, geometry

## Publishing to PyPI (Free Hosting)

To make this server easily installable anywhere:

1. Create a PyPI account at https://pypi.org/account/register/
2. Install build tools: `uv pip install build twine`
3. Build the package: `python -m build`
4. Upload to PyPI: `twine upload dist/*`

After publishing, anyone can install with: `pip install sf-parking-mcp`

## Development

```bash
# Install dev dependencies
uv sync

# Run server locally
uv run server.py

# Test with MCP inspector
npx @modelcontextprotocol/inspector uv run server.py
```

## License

MIT

## Contributing

Contributions welcome! Please open an issue or PR.
