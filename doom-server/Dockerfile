# Use a lightweight Debian base
FROM debian:bookworm-slim

# Prevent interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install Chocolate Doom ONCE during the build process
RUN apt-get update && \
    apt-get install -y chocolate-doom && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /data

# Default command to run the server
ENTRYPOINT ["chocolate-server"]
