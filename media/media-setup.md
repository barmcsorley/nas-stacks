# NAS Media Server Architecture: The "Split-Ingest" Model

**Context:** This setup runs on a UGreen NAS with a GitOps workflow. It solves the "Librarian Conflict" by allowing Readarr to manage Audiobooks while delegating Ebook management to Calibre-Web-Automated (CWA), all using a single download client.

## 1. Host Directory Structure

Ensure these folders exist on your NAS (`/volume1/SlowHDD`).

```text
/volume1/SlowHDD/
├── movies/                     # Managed by Radarr
├── tvseries/                   # Managed by Sonarr
├── books/
│   ├── audiobooks/             # Readarr moves audiobooks here. ABS reads from here.
│   └── calibreweblib/          # CWA manages this. Calibre Desktop & Readarr (Books) read from here.
└── downloads/
    ├── downloads/              # Default save path (Movies/TV go here)
    ├── books/                  # qBit "books" category saves here (Watched by CWA)
    └── audiobooks/             # qBit "audiobooks" category saves here (Watched by Readarr)

```

---

## 2. The "Golden Rule" for Docker Volumes

For **qBittorrent** and **Readarr** to manage multiple categories (Movies, Audio, Books) in parallel folders, they must map the **Parent Download Folder** (`/volume1/SlowHDD/downloads`), not just the subfolder.

* **Wrong:** `- /volume1/SlowHDD/downloads/downloads:/downloads` (Trapped in subfolder)
* **Correct:** `- /volume1/SlowHDD/downloads:/downloads` (Can see all siblings)

---

## 3. Service Configurations (Docker Compose)

### A. qBittorrent (The Source)

* **Role:** Downloads files. Sorts them into subfolders based on categories.
* **Internal Config (WebUI):**
* **Default Save Path:** `/downloads/downloads` (Crucial for Sonarr/Radarr compatibility).
* **Category `books`:** Save to `/downloads/books`.
* **Category `audiobooks`:** Save to `/downloads/audiobooks`.



```yaml
services:
  qbittorrent-vue:
    image: ghcr.io/linuxserver/qbittorrent:latest
    container_name: qBittorrent-VUE
    network_mode: host
    environment:
      - PUID=1000
      - PGID=10
      - WEBUI_PORT=9866
    volumes:
      - /volume2/FastSSD/docker/qbittorrent/config:/config:rw
      # CRITICAL: Maps the parent folder so it can create sibling folders
      - /volume1/SlowHDD/downloads:/downloads:rw
    restart: on-failure:5

```

### B. Readarr (The Manager)

* **Role:**
* **Audiobooks:** Search, Download, and **Import/Move** to library.
* **Ebooks:** Search & Download only (CWA handles import).


* **Settings:**
* **Root Folder (Audiobooks):** `/books/audiobooks`
* **Root Folder (Books):** `/books/calibreweblib` (Set to "Unmonitor Deleted" so it doesn't panic when CWA moves files).



```yaml
services:
  readarr:
    image: lscr.io/linuxserver/readarr:nightly-0.4.19.2811-ls400
    container_name: readarr
    environment:
      - PUID=1000
      - PGID=1000
    volumes:
      - /volume2/FastSSD/docker/readarr/config:/config
      # Library Access
      - /volume1/SlowHDD/books:/books
      # Download Access (Matches qBittorrent)
      - /volume1/SlowHDD/downloads:/downloads
    ports:
      - 8787:8787
    restart: unless-stopped

```

### C. Calibre-Web Automated & Downloader (The Ebook Ingesters)

* **Role:** Watches the specific download subfolder, imports books to the Calibre library, and deletes the source file.
* **Critical Fix:** Direct mapping to the book download folder (no redundant `/downloads` path).

```yaml
services:
  calibre-web-automated:
    image: crocodilestick/calibre-web-automated:latest
    container_name: Calibre-Web-Automated
    environment:
      - PUID=1000
      - PGID=100
      - DOCKER_MODS=linuxserver/mods:universal-calibre|linuxserver/mods:universal-package-install
    volumes:
      - /volume2/FastSSD/docker/calibrewebautomated/config:/config:rw
      # WATCH FOLDER: Points specifically to where qBit puts ebooks
      - /volume1/SlowHDD/downloads/books:/cwa-book-ingest:rw
      # LIBRARY: The final destination
      - /volume1/SlowHDD/books/calibreweblib:/calibre-library:rw
    ports:
      - 8213:8083
    restart: on-failure:5

  calibre-web-automated-book-downloader:
    image: ghcr.io/calibrain/calibre-web-automated-book-downloader:v1.0.4
    container_name: calibre-web-automated-book-downloader
    environment:
      - FLASK_PORT=8084
    volumes:
      # MATCHES the CWA ingest folder exactly
      - /volume1/SlowHDD/downloads/books:/cwa-book-ingest
    ports:
      - 8084:8084
    restart: unless-stopped

```

### D. Audiobookshelf (The Player)

* **Role:** Streams media. Treats folders as Read-Only to prevent messing up Readarr's file management.

```yaml
services:
  audiobookshelf:
    image: advplyr/audiobookshelf:latest
    container_name: Audiobookshelf
    volumes:
      - /volume2/FastSSD/docker/audiobookshelf:/config:rw
      - /volume2/FastSSD/docker/audiobookshelf/metadata:/metadata:rw
      # EBOOKS: Reads the CWA library
      - /volume1/SlowHDD/books/calibreweblib:/books:ro
      # AUDIOBOOKS: Reads the Readarr library
      - /volume1/SlowHDD/books/audiobooks:/audiobooks:ro
    ports:
      - 13378:80
    restart: on-failure:5

```
