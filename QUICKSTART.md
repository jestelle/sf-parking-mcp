# Quick Start Guide

## 1. Test Locally (2 minutes)

```bash
# Install dependencies
uv sync

# Test the API works
uv run test_api.py

# Run the MCP server (Ctrl+C to stop)
uv run server.py
```

## 2. Configure Claude Desktop (2 minutes)

**MacOS**: Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: Edit `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "sf-parking": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/joshestelle/tools/sf-parking",
        "run",
        "server.py"
      ]
    }
  }
}
```

**Important**: Change `/Users/joshestelle/tools/sf-parking` to your actual path!

Restart Claude Desktop.

## 3. Try It Out

Ask Claude:
- "What parking is available on 2nd Avenue in SF?"
- "Find me parking near coordinates 37.7833, -122.4602"
- "Show parking between lat 37.78-37.79 and lon -122.47 to -122.46"

## 4. Deploy (Optional - 10 minutes)

Want others to use your server? See [DEPLOYMENT.md](DEPLOYMENT.md) for free hosting options.

**Easiest**: Publish to PyPI (free), then anyone can install with:
```bash
pip install sf-parking-mcp
```

## Troubleshooting

**Server not showing in Claude Desktop?**
- Make sure you saved the config file
- Restart Claude Desktop completely
- Check the path is absolute (not relative)

**API returning no data?**
- The SF parking API may be empty at times
- Run `uv run test_api.py` to verify connectivity

**uv command not found?**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
