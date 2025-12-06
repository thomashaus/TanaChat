# DigitalOcean Deployment Guide

## 🚀 Deploy TanaChat to DigitalOcean

This guide covers deploying TanaChat to DigitalOcean App Platform and Container Registry.

## ⚠️ Security Notice

**NEVER commit real credentials to your repository!** Always use DigitalOcean's built-in secrets management or GitHub Secrets.

## Prerequisites

1. DigitalOcean account with billing enabled
2. doctl installed locally
3. GitHub repository access
4. Domain name (optional)

## Step 1: Set Up DigitalOcean Container Registry

```bash
# Install doctl
brew install doctl  # macOS
# or
curl -sL https://github.com/digitalocean/doctl/releases/latest/download/doctl-$(uname -s)-$(uname -m).tar.gz | tar xz
sudo mv doctl /usr/local/bin/

# Authenticate
doctl auth init
```

## Step 2: Configure GitHub Secrets

In your GitHub repository, go to Settings → Secrets and variables → Actions and add:

- `DIGITALOCEAN_ACCESS_TOKEN`: Your DigitalOcean API token
- `SPACES_ACCESS_KEY`: Your Spaces access key
- `SPACES_SECRET_KEY`: Your Spaces secret key
- `TANA_API_KEY`: Your Tana API key

## Step 3: Deploy the Application

### Option A: Automatic Deployment (Recommended)

1. Push to main branch
2. GitHub Actions will automatically build and deploy
3. Monitor deployment in the Actions tab

### Option B: Manual Deployment

```bash
# Build and push images
docker buildx build --platform linux/amd64,linux/arm64 -t registry.digitalocean.com/espresso/TanaChat-app:latest ./app
docker buildx build --platform linux/amd64,linux/arm64 -t registry.digitalocean.com/espresso/TanaChat-mcp:latest ./mcp

# Push to registry
docker push registry.digitalocean.com/espresso/TanaChat-app:latest
docker push registry.digitalocean.com/espresso/TanaChat-mcp:latest

# Deploy using doctl
doctl apps create --spec app-do.yaml
doctl apps create --spec mcp-do.yaml
```

## Step 4: Configure Environment Variables

In DigitalOcean App Platform dashboard:

1. Go to your app settings
2. Add the following environment variables:

**For TanaChat-app:**
```
NODE_ENV=production
VITE_API_URL=https://your-app-url.ondigitalocean.app
```

**For TanaChat-mcp:**
```
PYTHON_VERSION=3.12
S3_BUCKET=tanachat
S3_REGION=nyc3
S3_ENDPOINT=https://nyc3.digitaloceanspaces.com
TANA_API_KEY=[Add as secret]
SPACES_ACCESS_KEY=[Add as secret]
SPACES_SECRET_KEY=[Add as secret]
```

## Step 5: Set Up Custom Domain (Optional)

1. Add your domain to DigitalOcean
2. Configure DNS records
3. Update app routes in the app specification

## Step 6: Verify Deployment

1. Check app health: https://your-app-url.ondigitalocean.app/health
2. Check MCP server: https://your-mcp-url.ondigitalocean.app/health
3. Test the web interface
4. Verify API connectivity

## Troubleshooting

### Build Failures
- Check the GitHub Actions logs
- Verify Dockerfile paths are correct
- Ensure all dependencies are listed

### Runtime Errors
- Check app logs in DigitalOcean dashboard
- Verify environment variables are set
- Ensure Spaces credentials have proper permissions

### Permission Issues
- Verify API token has required scopes
- Check Spaces bucket permissions
- Ensure app has access to required resources

## Production Checklist

- [ ] Rotate any exposed credentials
- [ ] Enable monitoring and alerts
- [ ] Set up backup for Spaces
- [ ] Configure SSL certificates
- [ ] Set up logging
- [ ] Configure rate limiting
- [ ] Test disaster recovery

## Support

- DigitalOcean Documentation: https://docs.digitalocean.com/
- GitHub Issues: https://github.com/thomashaus/TanaChat/issues
- Discussions: https://github.com/thomashaus/TanaChat/discussions