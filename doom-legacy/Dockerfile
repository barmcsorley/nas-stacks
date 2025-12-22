FROM debian:bookworm-slim@sha256:e899040a73d36e2b36fa33216943539d9957cba8172b858097c2cabcdb20a3e2

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# CRITICAL FIX: Add /usr/games to the system path so it finds the executable
ENV PATH="/usr/games:${PATH}"

# Install the game and clean up apt cache to keep image small
RUN apt-get update && \
    apt-get install -y chocolate-doom && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /data

# Default entrypoint
ENTRYPOINT ["chocolate-server"]