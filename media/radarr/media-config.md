Here is your complete **GitOps Media Stack Configuration** cheat sheet.

This serves as the "Source of Truth" for your naming standards, quality profiles, and server connections.

---

# Media Stack Configuration (Radarr / Sonarr / Plex / Jellyfin / Overseerr / Jellyseerr / Trakt)

**Updated:** January 2026
**Architecture:** GitOps (Docker Compose + Renovate)
**Storage:** UGreen NAS (`/volume2/FastSSD/media`)

---

## 1. Radarr Configuration (Movies)

**Settings > Media Management**

* **Rename Movies:** ✅ Enabled
* **Replace Illegal Characters:** ✅ Enabled
* **Colon Replacement:** "Replace with Space Dash" (`-`)

| Setting | Format String (Trash Guides Standard) |
| --- | --- |
| **Standard Movie Format** | `{Movie CleanTitle} ({Release Year}) {edition-{Edition Tags}} [imdbid-{ImdbId}] {[Custom Formats]}{ [Quality Full]}{ [MediaInfo 3D]}{ [MediaInfo VideoDynamicRangeType]}{ [{MediaInfo VideoBitDepth}bit]}{ [MediaInfo VideoCodec]}{ [MediaInfo AudioCodec]}{ [MediaInfo AudioChannels]}{ [MediaInfo AudioLanguages]} - {Release Group}` |
| **Movie Folder Format** | `{Movie CleanTitle} ({Release Year}) [imdbid-{ImdbId}]` |

**Settings > Metadata**

* **Provider:** Kodi (XBMC) / Emby
* **Enable:** ✅
* **Metadata (NFO):** ✅
* **Images:** ✅

---

## 2. Sonarr Configuration (TV Series)

**Settings > Media Management**

* **Rename Episodes:** ✅ Enabled

| Setting | Format String (Trash Guides Standard) |
| --- | --- |
| **Series Folder Format** | `{Series TitleYear} {tvdb-{TvdbId}}` |
| **Season Folder Format** | `Season {season:00}` |
| **Standard Episode Format** | `{Series TitleYear} - S{season:00}E{episode:00} - {Episode CleanTitle} {[Custom Formats]}{ [Quality Full]}{ [MediaInfo VideoDynamicRangeType]}{ [{MediaInfo VideoBitDepth}bit]}{ [MediaInfo VideoCodec]}{ [MediaInfo AudioCodec]}{ [MediaInfo AudioChannels]}{ [MediaInfo AudioLanguages]} - {Release Group}` |
| **Daily Episode Format** | `{Series Title} - {Air-Date} - {Episode CleanTitle} {[Custom Formats]}{ [Quality Full]}{ [MediaInfo VideoDynamicRangeType]}{ [{MediaInfo VideoBitDepth}bit]}{ [MediaInfo VideoCodec]}{ [MediaInfo AudioCodec]}{ [MediaInfo AudioChannels]}{ [MediaInfo AudioLanguages]} - {Release Group}` |
| **Anime Episode Format** | `{Series TitleYear} - S{season:00}E{episode:00} - {Episode CleanTitle} {[Custom Formats]}{ [Quality Full]}{ [MediaInfo VideoDynamicRangeType]}{ [{MediaInfo VideoBitDepth}bit]}{ [MediaInfo VideoCodec]}{ [MediaInfo AudioCodec]}{ [MediaInfo AudioChannels]}{ [MediaInfo AudioLanguages]} - {Release Group}` |

**Settings > Metadata**

* **Provider:** Kodi (XBMC) / Emby
* **Enable:** ✅
* **Metadata (NFO):** ✅
* **Images:** ✅
* **Season Images:** ✅

---

## 3. Recyclarr (Quality Profiles)

**Docker Compose Service:**

```yaml
services:
  recyclarr:
    image: ghcr.io/recyclarr/recyclarr:latest
    container_name: recyclarr
    user: 1000:1000
    volumes:
      - /volume2/FastSSD/docker/recyclarr/config:/config
    env_file: .env
    restart: unless-stopped

```

**Configuration (`/config/recyclarr.yml`):**
*Note: Using LAN IP ensures connectivity across separate Docker stacks.*

```yaml
sonarr:
  tv-series:
    base_url: http://192.168.68.XXX:8989
    api_key: !env_var SONARR_API_KEY
    include:
      - template: sonarr-quality-definition-series
      - template: sonarr-v4-quality-profile-web-1080p

radarr:
  movies:
    base_url: http://192.168.68.XXX:7878
    api_key: !env_var RADARR_API_KEY
    include:
      - template: radarr-quality-definition-movie
      - template: radarr-quality-profile-hd-bluray-web

```

---

## 4. Media Server Settings

### Jellyfin

* **Port:** `8097` (Due to Emby conflict on 8096)
* **NFO Settings:** Enable NFO Reading ✅ | Enable NFO Saving ❌
* **Library Settings (Movies & TV):**
* **Metadata Downloaders:** Uncheck ALL (Force NFO use).
* **Image Fetchers:** Uncheck ALL (Force local assets use).



### Plex

* **Port:** `32400`
* **Library Settings (Edit > Advanced):**
* **Scanner/Agent:** Plex Movie
* **Use Local Assets:** ✅ (Critical for Posters)
* **Prefer Local Metadata:** ✅



---

## 5. Automation Connections (Instant Scan)

**In Radarr / Sonarr > Settings > Connect:**

| Connection Name | Protocol | Host / IP | Port | Notes |
| --- | --- | --- | --- | --- |
| **Jellyfin Update** | Jellyfin | `192.168.68.XXX` | **8097** | Requires Admin API Key |
| **Plex Update** | Plex | `192.168.68.XXX` | **32400** | Requires X-Plex-Token |
---


Here is the comprehensive documentation for your "Belfast Media Stack." This summary captures the architecture, service roles, and specific configurations we have built. You can save this in your GitHub repository as `README.md` for future reference.

### 1. The Architecture Overview

This stack follows a **GitOps** model. All configuration (Docker Compose, Recyclarr YAML) is version-controlled in GitHub. Updates are handled via **Renovate**, and deployment is managed by **Portainer** on your UGreen NAS.

**The Workflow:**

1. **Request:** Family requests media via **Jellyseerr** (or Overseerr).
2. **Manager:** **Radarr/Sonarr** grabs the request and consults Recyclarr profiles.
3. **Indexer:** **Prowlarr** (via FlareSolverr) searches torrent sites.
4. **Download:** **qBittorrent** downloads the file via **GlueTun** (VPN).
5. **Import:** Radarr/Sonarr hardlinks the file to `/movies` or `/tv`.
6. **Playback:** **Jellyfin** (or Plex) streams the content.
7. **Sync:** **Trakt** syncs watched status across all platforms.

---

### 2. The Service Stack

| Service | Role | Key Configuration |
| --- | --- | --- |
| **qBittorrent** | Downloader | • Global Ratio Limit: 1.0 (Pause)<br>

<br>• Category: `radarr`/`sonarr`<br>

<br>• Network: Uses GlueTun container |
| **Radarr** | Movies | • Profile: `HD Bluray + WEB` (1080p)<br>

<br>• Quality Sliders: Manual (e.g., 5 GiB/h) |
| **Sonarr** | TV Shows | • Profile: `WEB-1080p`<br>

<br>• Quality Sliders: Manual (Recyclarr templates disabled) |
| **Prowlarr** | Indexer Manager | • Syncs indexers to Radarr/Sonarr<br>

<br>• Uses FlareSolverr for Cloudflare bypass |
| **Recyclarr** | Config Manager | • Manages Custom Formats (Audio/Video scoring)<br>

<br>• *Note:* Quality Definitions disabled to allow manual slider control |
| **Overseerr** | Request (Plex) | • Port: `5055`<br>

<br>• Region: UK<br>

<br>• 1080p Forced Default |
| **Jellyseerr** | Request (Jellyfin) | • Port: `5056`<br>

<br>• Linked to Jellyfin Users<br>

<br>• Request Limit: 2/week (Kids) |
| **PlexTraktSync** | Sync Bridge | • `command: watch`<br>

<br>• Syncs Plex  Trakt |
| **Jellyfin** | Media Player | • **Trakt Plugin** installed (Native) for sync |

---

### 3. "The Secret Sauce" (Custom Configurations)

These are the specific tweaks that make your system robust and family-friendly.

#### A. The "Anti-4K" Safety Net

To prevent massive 23GB+ downloads:

1. **Recyclarr:** `recyclarr.yml` manages quality *profiles* but has `quality-definition` templates commented out.
2. **Radarr/Sonarr:** Quality sliders are manually set to **~5-8 GiB/h**.
3. **Overseerr/Jellyseerr:**
* Default Profile: **HD Bluray + WEB** (1080p).
* User Permissions: `Request: Advanced` is **disabled** for kids (they cannot choose 4K).



#### B. The Trakt Bridge (Sync)

Since you run a dual-ecosystem (Plex + Jellyfin), "Watched" status is synced via Trakt.

* **Jellyfin:** Uses the native **Trakt Plugin** (Scheduled Task + Scrobble).
* **Plex:** Uses the **PlexTraktSync** container running in `watch` mode.
* **Flow:** User watches on Jellyfin  Plugin updates Trakt  PlexTraktSync updates Plex.

#### C. The "Netflix" Experience

* **Discovery:** Region set to **United Kingdom** in Overseerr/Jellyseerr to show correct streaming links (BBC iPlayer, Netflix UK).
* **Availability:** "Mark as Available" feature used for content you own on Amazon/Netflix to prevent unnecessary downloads.

---

### 4. Maintenance & Operations

#### Adding a New User

1. Create the user in **Jellyfin** (or Plex).
2. User logs into **Jellyseerr** (or Overseerr) with those credentials.
3. **Admin Action:** Go to Jellyseerr > Users > Permissions.
* Uncheck `Request: Advanced`.
* Set Request Quota (e.g., 2).



#### Preventing "Downloads" for Streaming Content

If a show is on BBC iPlayer/Netflix:

1. Find the show in Jellyseerr.
2. Click the **Wrench/Gear Icon** (Top Right).
3. Select **Mark as Available**.
4. Result: Show turns "Green" for the family; nothing is downloaded.

#### Handling Updates

* **Containers:** Handled automatically by your **Renovate** bot in GitHub.
* **Recyclarr:** updates Custom Formats automatically on schedule.
* **Sliders:** You must adjust these manually in Radarr/Sonarr if you ever want to change file size limits (Recyclarr will not touch them).

### 5. Next Steps

Your stack is now fully operational, automated, and "teenager-proofed."

* **Immediate Action:** Ensure you have committed the final `docker-compose.yaml` (with `plextraktsync` and `jellyseerr`) to your GitHub repo.
* **Optional Future Upgrade:** If you ever face "Cookie Conflicts" (logging out) again, we can look at adding **Nginx Proxy Manager** to give your services nice names like `requests.lan` and `jellyfin.lan`.

Would you like me to help you set up that Nginx Proxy Manager now, or are you happy to let the system run as is for a while?
**Next Step:** I can leave you to it now! Your system is fully optimized. If you ever need to troubleshoot a specific container or log in the future, just ping me. Enjoy the movies!
