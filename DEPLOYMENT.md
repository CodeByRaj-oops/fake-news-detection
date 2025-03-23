# Fake News Detection System - Deployment Guide

This guide outlines multiple ways to deploy the Fake News Detection System, from local development to production deployment options.

## Table of Contents

- [Local Development](#local-development)
- [Single-Server Deployment](#single-server-deployment)
- [Docker Deployment](#docker-deployment)
- [Production Considerations](#production-considerations)

## Local Development

For local development, use our simplified starter script:

```bash
.\simple-start.cmd
```

This will:
1. Install required dependencies
2. Start the backend on port 8000
3. Start the frontend on port 3000

Access the application at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## Single-Server Deployment

For simple production deployment on a single server:

```bash
.\deploy-single-server.cmd
```

This creates a production-ready deployment in the `deployment` directory with:
1. Built frontend files
2. Configured backend
3. Combined server script
4. Single entry point

To run the deployed application:
```bash
cd deployment
.\start-server.cmd
```

Access the application at http://localhost:8000

### Requirements

- Python 3.7+
- Node.js 14+
- 2GB RAM minimum
- 1GB free disk space

## Docker Deployment

For containerized deployment:

```bash
.\docker-deploy.cmd
```

This will:
1. Build a Docker image containing both frontend and backend
2. Start a Docker container running the application
3. Configure volumes for persistent data

Access the application at http://localhost:8000

### Manual Docker Deployment

If you prefer to run Docker commands manually:

```bash
# Build the image
docker build -t fake-news-detector .

# Run the container
docker run -p 8000:8000 -v ./data:/app/backend/models -v ./logs:/app/logs fake-news-detector
```

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Production Considerations

For real production deployment, consider:

### Security

1. Replace wildcard CORS (`*`) with specific domains in production
2. Set up proper authentication
3. Implement rate limiting
4. Configure HTTPS using a reverse proxy

### Server Setup

1. Use a reverse proxy (Nginx, Apache) in front of the application
2. Set up process management with PM2 or systemd
3. Configure automatic restarts
4. Set up health monitoring

### Example Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### HTTPS Setup with Certbot

```bash
# Install Certbot
apt-get install certbot python3-certbot-nginx

# Obtain and install certificate
certbot --nginx -d your-domain.com
```

### Process Management with PM2

```bash
# Install PM2
npm install -g pm2

# Start application with PM2
cd deployment
pm2 start server.py --name "fake-news-detector" --interpreter python

# Set up startup script
pm2 startup
pm2 save
```

## Troubleshooting

### Connection Issues

If the frontend cannot connect to the backend:

1. Check if the backend server is running
2. Verify CORS settings in app_new.py
3. Ensure ports are not blocked by firewalls
4. Check logs for specific errors

### Resource Issues

If the application crashes or performs poorly:

1. Increase the memory allocated to the application (particularly for Docker)
2. Check disk space for logs and model files
3. Consider scaling horizontally for production workloads

## Scaling Up

For higher traffic scenarios:

1. Deploy the backend to multiple servers behind a load balancer
2. Host the frontend on a CDN
3. Use a dedicated database for storing analysis results
4. Implement caching for frequently requested analyses 