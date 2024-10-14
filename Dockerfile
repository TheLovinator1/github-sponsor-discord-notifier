FROM python:3.13

# Create a non-root user for security
RUN useradd --create-home botuser

# Switch to the new user
USER botuser

# Set the working directory
WORKDIR /home/botuser/github-sponsors-discord-notifier

# Copy project files
COPY --chown=botuser:botuser main.py requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Add to path
ENV PATH="/home/botuser/.local/bin:${PATH}"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Expose the port the app will run on
EXPOSE 5000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--proxy-headers"]
