FROM debian:bookworm-slim@sha256:98f4b71de414932439ac6ac690d7060df1f27161073c5036a7553723881bffbe

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