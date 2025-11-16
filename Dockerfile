# Dockerfile
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy and install dependencies
COPY pyproject.toml .
# To this (add --system):
RUN uv pip install -r pyproject.toml --system

# Copy the startup script and make it executable
COPY ./docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Copy the rest of the app (the . in volumes will overwrite this,
# but it's good practice to have it here for non-dev builds)
COPY . /app

# Run the entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]