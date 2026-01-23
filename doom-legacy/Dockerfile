FROM debian:bookworm-slim@sha256:56ff6d36d4eb3db13a741b342ec466f121480b5edded42e4b7ee850ce7a418ee

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