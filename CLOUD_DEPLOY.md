# Deploy Your SF Parking MCP Server to the Cloud

## Option 1: Google Cloud Run (Recommended - Free Tier)

### Prerequisites
- Google Cloud account (free tier available)
- `gcloud` CLI installed

### Step-by-Step Deployment

#### 1. Install gcloud CLI (if needed)
```bash
# macOS
brew install google-cloud-sdk

# Or download from: https://cloud.google.com/sdk/docs/install
```

#### 2. Login and setup
```bash
# Login to Google Cloud
gcloud auth login

# Create a new project (or use existing)
gcloud projects create sf-parking-mcp --name="SF Parking MCP"

# Set the project
gcloud config set project sf-parking-mcp

# Enable Cloud Run API
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

#### 3. Deploy!
```bash
cd /Users/joshestelle/tools/sf-parking

# Deploy to Cloud Run (builds from Dockerfile automatically)
gcloud run deploy sf-parking-mcp \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000
```

That's it! You'll get a URL like: `https://sf-parking-mcp-xxxxx.run.app`

#### 4. Test your deployment
```bash
curl https://YOUR-URL.run.app/mcp
```

#### 5. Use in Claude Desktop
```json
{
  "mcpServers": {
    "sf-parking": {
      "url": "https://YOUR-URL.run.app/mcp"
    }
  }
}
```

### Cost
- **FREE** for up to 2 million requests/month
- Auto-scales to zero (no cost when not in use)
- Perfect for personal MCP servers!

---

## Option 2: Railway (Also Free Tier)

### Step-by-Step

#### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

#### 2. Login
```bash
railway login
```

#### 3. Deploy
```bash
cd /Users/joshestelle/tools/sf-parking
railway init
railway up
```

#### 4. Get your URL
```bash
railway domain
```

### Cost
- **FREE** $5 credit/month
- Enough for continuous running

---

## Option 3: Render (Free Tier)

### Step-by-Step

#### 1. Create account at https://render.com

#### 2. Connect GitHub repo
- New > Web Service
- Connect your GitHub repo
- Select `sf-parking-mcp`

#### 3. Configure
- **Build Command**: `pip install uv && uv sync`
- **Start Command**: `uv run fastmcp_server.py --http`
- **Port**: 8000

#### 4. Deploy
Click "Create Web Service" - done!

### Cost
- **FREE** tier available
- Spins down after 15 min of inactivity

---

## Option 4: Fly.io (Free Tier)

### Step-by-Step

#### 1. Install flyctl
```bash
# macOS
brew install flyctl

# Or: curl -L https://fly.io/install.sh | sh
```

#### 2. Login
```bash
flyctl auth login
```

#### 3. Launch
```bash
cd /Users/joshestelle/tools/sf-parking
flyctl launch

# Answer prompts:
# - App name: sf-parking-mcp
# - Region: Choose closest to you
# - Deploy now: Yes
```

#### 4. Get URL
```bash
flyctl status
```

Your app will be at: `https://sf-parking-mcp.fly.dev`

### Cost
- **FREE** for 3 shared VMs
- Always-on, no sleep

---

## Comparison

| Service | Free Tier | Setup Time | Always-On | Recommendation |
|---------|-----------|------------|-----------|----------------|
| **Google Cloud Run** | 2M req/month | 5 min | No (auto-scale) | ⭐ Best overall |
| **Railway** | $5 credit/mo | 3 min | Yes | Good for testing |
| **Render** | Limited | 5 min | No (sleeps) | Easy but slow |
| **Fly.io** | 3 VMs | 5 min | Yes | Great for prod |

## My Recommendation

**Start with Google Cloud Run** - it's:
- Most generous free tier
- Best integration with FastMCP
- Auto-scaling (only pay for usage)
- Professional and reliable

The single command deployment is:
```bash
gcloud run deploy sf-parking-mcp --source . --region us-central1 --allow-unauthenticated --port 8000
```

That's it! You'll have a live MCP server in minutes! 🚀
