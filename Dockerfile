FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY pyproject.toml .
RUN pip install --no-cache-dir fastmcp httpx

# Copy server file
COPY fastmcp_server.py .

# Expose port
EXPOSE 8000

# Run server with HTTP transport
CMD ["python", "fastmcp_server.py", "--http"]
