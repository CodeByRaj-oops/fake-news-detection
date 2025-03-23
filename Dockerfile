# Use multi-stage build for smaller final image
FROM node:16-alpine AS frontend-build

# Build frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Main image with Python
FROM python:3.9-slim

# Create app directory
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p backend/reports backend/history backend/models backend/utils

# Copy backend files
COPY backend/*.py backend/
COPY backend/utils/*.py backend/utils/

# Copy frontend build from first stage
COPY --from=frontend-build /app/frontend/build frontend/

# Copy server script
COPY deployment/server.py ./

# Expose port
EXPOSE 8000

# Set environment variables
ENV PORT=8000
ENV HOST=0.0.0.0

# Start server
CMD ["python", "server.py"] 