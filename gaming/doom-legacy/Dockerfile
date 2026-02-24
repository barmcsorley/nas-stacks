FROM debian:bookworm-slim@sha256:74d56e3931e0d5a1dd51f8c8a2466d21de84a271cd3b5a733b803aa91abf4421

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