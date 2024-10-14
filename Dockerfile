# Use a minimal base image for Python
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    DEBIAN_FRONTEND=noninteractive

# Update the system, install dependencies, and clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    mv "$HOME/.local" "$POETRY_HOME" && \
    ln -s "$POETRY_HOME/bin/poetry" /usr/local/bin/poetry && \
    rm -rf /tmp/*

# Create a non-root user for security
RUN useradd --create-home botuser

# Switch to the new user
USER botuser

# Set the working directory
WORKDIR /home/botuser/github-sponsors-discord-notifier

# Copy project files
COPY --chown=botuser:botuser pyproject.toml README.md LICENSE main.py ./

# Install dependencies
RUN /opt/poetry/bin/poetry install --no-dev --no-interaction --no-ansi && \
    rm -rf "$POETRY_HOME/cache"

# Expose the port the app will run on
EXPOSE 5000

# Start the application
CMD ["/opt/poetry/bin/poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--proxy-headers"]
