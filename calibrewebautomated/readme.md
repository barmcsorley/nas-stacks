Here is the comprehensive technical documentation for your setup. It documents the specific "patches" we applied to make Calibre 8 stable on your NAS, so you don't have to rediscover them.

Calibre-Web Automated: Stability & Maintenance Guide
System: UGreen NAS / Docker / GitOps
Calibre Version: v8.x (Qt6 Engine)
Database Engine: SQLite
1. Production Configuration (docker-compose.yaml)
This configuration runs as the standard user (PUID: 1000) but injects critical system libraries required by the Calibre v8 Qt6 engine. Without INSTALL_PACKAGES, the container will crash with a libasound or NoneType database error.

YAML


services:
  calibre-web-automated:
    image: crocodilestick/calibre-web-automated:latest
    container_name: Calibre-Web-Automated
    environment:
      # User Permissions (matches NAS 'users' group)
      PUID: 1000
      PGID: 100
      TZ: Europe/Dublin
      
      # TOKEN: Managed in Portainer UI Environment Variables
      HARDCOVER_TOKEN: ${HARDCOVER_TOKEN}

      # CRITICAL STABILITY FIX
      # 1. 'universal-package-install' allows us to inject OS-level libraries on boot.
      # 2. 'INSTALL_PACKAGES' lists the Qt6 dependencies missing from the base image.
      DOCKER_MODS: linuxserver/mods:universal-calibre|linuxserver/mods:universal-package-install
      INSTALL_PACKAGES: libasound2|libxkbcommon-x11-0|libegl1|libopengl0|libglx0|libnss3|libxcomposite1|libxdamage1|libxrandr2|libxtst6|libxcursor1|libxi6
    
    volumes:
      - /volume2/FastSSD/docker/calibrewebautomated/config:/config:rw
      - /volume2/FastSSD/docker/cwabookdownloader/ingest:/cwa-book-ingest:rw
      - /volume1/SlowHDD/books/calibreweblib:/calibre-library:rw
      - /volume2/FastSSD/docker/calibrewebautomated/plugins:/config/.config/calibre/plugins:rw
    ports:
      - 8213:8083
    restart: on-failure:5
    healthcheck:
      test: ["CMD-SHELL", "nc -z 127.0.0.1 8083 || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 90s


2. Database Integrity Rules
Because SQLite is a file-based database, it is highly susceptible to corruption if accessed by multiple sources or synced incorrectly.
Rule 1: The "Single Writer" Protocol
Never open the Calibre Desktop application (on Windows/Mac) while the Docker container is running.
To Edit Manually: Stop Container -> Open Desktop App -> Edit -> Close Desktop App -> Start Container.
Rule 2: Syncthing Ignore Patterns
To prevent file locking conflicts which cause 500 Internal Server Errors, add these patterns to the .stignore file for your library folder:

Plaintext


# Ignore SQLite temporary lock files
metadata.db-wal
metadata.db-shm

# Ignore Syncthing conflict files
*sync-conflict*

# Ignore temporary/partial files
*.tmp


3. Troubleshooting
If the Web UI crashes with 500 Internal Server Error, follow this recovery procedure:
Scenario A: "Multiple metadata.db files found"
Check logs for the exact name of the duplicate file (usually .syncthing... or .windows_fail).
Delete the duplicate file via SSH.
Restart container.
Scenario B: Database Corruption (NoneType error)
Stop the container.
Move the corrupted database: mv metadata.db metadata.db.bak
Start the container (it will create a fresh, empty DB).
Run the restore command via SSH to rebuild the DB from book files:
Bash
docker exec -it Calibre-Web-Automated calibredb restore_database --really-do-it --with-library /calibre-library


