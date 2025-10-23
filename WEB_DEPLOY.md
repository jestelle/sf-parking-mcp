# Web Deployment Complete! 🎉

Your MCP server is now hosted at:
**https://sf-parking-qwevge6jc-jestelles-projects.vercel.app**

## How to Use Your Hosted MCP Server

Add this to your Claude Desktop configuration:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "sf-parking": {
      "url": "https://sf-parking-qwevge6jc-jestelles-projects.vercel.app/sse"
    }
  }
}
```

Restart Claude Desktop and you're done!

## What You Got

✓ **Free hosting** on Vercel (no credit card required)
✓ **Global CDN** - fast from anywhere
✓ **Auto-scaling** - handles any load
✓ **HTTPS** - secure by default
✓ **Zero maintenance** - no servers to manage

## Future Updates

To update your deployed server:

```bash
cd /Users/joshestelle/tools/sf-parking
git add .
git commit -m "Update server"
git push
vercel deploy --prod --yes
```

Vercel will automatically rebuild and deploy!

## Custom Domain (Optional)

Want a cleaner URL like `sf-parking.yourdomain.com`?
1. Go to https://vercel.com/jestelles-projects/sf-parking/settings/domains
2. Add your custom domain
3. Update the Claude Desktop config with your new URL

## Troubleshooting

**Server not responding?**
Check logs: `vercel logs https://sf-parking-qwevge6jc-jestelles-projects.vercel.app`

**Need to redeploy?**
`vercel deploy --prod --yes`

## Cost

FREE forever on Vercel's Hobby plan:
- Unlimited requests
- 100GB bandwidth/month
- Serverless function execution included

Perfect for personal MCP servers!
