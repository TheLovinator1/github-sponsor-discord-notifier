# Use a minimal base image for Python
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="$POETRY_HOME/bin:$PATH" \
    DEBIAN_FRONTEND=noninteractive

# Install essential packages and curl for downloading Poetry, then clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get purge -y --auto-remove curl && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create a non-root user to enhance security
RUN useradd --create-home botuser

# Switch to the non-root user
USER botuser

# Set working directory to the new user's home directory
WORKDIR /home/botuser/github-sponsors-discord-notifier

# Copy the required files with appropriate permissions
COPY --chown=botuser:botuser pyproject.toml README.md LICENSE main.py ./

# Install only the necessary dependencies from Poetry
RUN poetry install --no-dev --no-interaction --no-ansi && \
    rm -rf "$POETRY_HOME/cache"

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
