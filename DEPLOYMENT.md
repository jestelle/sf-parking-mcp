# Free Deployment Options for SF Parking MCP Server

## Option 1: PyPI (Recommended - Free & Easiest)

This is the easiest way to make your MCP server available everywhere.

### Setup Steps:

1. **Create a PyPI account** (free): https://pypi.org/account/register/

2. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/sf-parking-mcp.git
   git push -u origin main
   ```

3. **Create a GitHub Release**:
   - Go to your repo: `https://github.com/YOUR_USERNAME/sf-parking-mcp`
   - Click "Releases" → "Create a new release"
   - Tag: `v0.1.0`
   - Title: `v0.1.0`
   - Click "Publish release"

4. **Add PyPI Token to GitHub** (one-time setup):
   - Go to PyPI: https://pypi.org/manage/account/token/
   - Create a new token (scope: "Entire account")
   - Copy the token
   - Go to GitHub repo → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: paste your token
   - Click "Add secret"

5. **The GitHub Action will automatically publish to PyPI!**

Now anyone can install your server with:
```bash
pip install sf-parking-mcp
```

## Option 2: Direct from GitHub (Free)

Users can install directly from your repo:

```bash
pip install git+https://github.com/YOUR_USERNAME/sf-parking-mcp.git
```

Or with uv:
```bash
uv pip install git+https://github.com/YOUR_USERNAME/sf-parking-mcp.git
```

Claude Desktop config:
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

## Option 3: Local Development (Free)

Just run locally without publishing:

1. Clone the repo
2. Install with uv: `uv sync`
3. Configure Claude Desktop with full path:

```json
{
  "mcpServers": {
    "sf-parking": {
      "command": "uv",
      "args": [
        "--directory",
        "/full/path/to/sf-parking",
        "run",
        "server.py"
      ]
    }
  }
}
```

## Cost Comparison

| Option | Hosting Cost | Setup Time | Distribution |
|--------|-------------|------------|--------------|
| PyPI   | FREE        | 10 min     | Global (best) |
| GitHub | FREE        | 5 min      | Anyone with git |
| Local  | FREE        | 2 min      | Just you |

**Recommendation**: Go with PyPI (Option 1) - it's free, professional, and easiest for users.
