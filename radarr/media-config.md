Here is your complete **GitOps Media Stack Configuration** cheat sheet.

This serves as the "Source of Truth" for your naming standards, quality profiles, and server connections.

---

# Media Stack Configuration (Radarr / Sonarr / Plex / Jellyfin)

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

**Next Step:** I can leave you to it now! Your system is fully optimized. If you ever need to troubleshoot a specific container or log in the future, just ping me. Enjoy the movies!
