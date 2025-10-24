FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy files
COPY fastmcp_server.py .
COPY pyproject.toml .
COPY uv.lock .

# Install dependencies
RUN uv sync

# Expose port
EXPOSE 8000

# Run server with HTTP transport
CMD ["uv", "run", "fastmcp_server.py", "--http"]
