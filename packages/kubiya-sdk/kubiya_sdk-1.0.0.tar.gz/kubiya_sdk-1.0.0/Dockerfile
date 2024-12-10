# Use an official Python runtime as the base image
FROM python:3.11-slim-buster
COPY --from=ghcr.io/astral-sh/uv:0.4.22 /uv /uvx /bin/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    git \
    libpq-dev \
    python3-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY uv.lock .
COPY pyproject.toml .
COPY README.md .

RUN uv sync --all-extras --frozen

# Add virtual environment to $PATH
ENV PATH="/app/.venv/bin:$PATH"

ENV PYTHONPATH="/app"

# Copy the SDK source code
COPY kubiya_sdk /app/kubiya_sdk

# Set the entrypoint to the CLI script
ENTRYPOINT ["python", "kubiya_sdk/cli.py", "server"]
