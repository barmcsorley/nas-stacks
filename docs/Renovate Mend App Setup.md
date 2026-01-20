# 🔄 Automated Update Strategy (Renovate)

This repository uses a **GitOps** model to manage Docker container updates. Instead of manually pulling images or using Watchtower, we use **Renovate (via Mend.io)** to scan for updates, create Pull Requests (PRs), and trigger our deployment pipeline.

## 🛠 Architecture Overview

1.  **Detection:** Renovate runs hourly, scanning all `docker-compose.yaml` files for outdated Docker images.
2.  **Reporting:** Pending updates are listed in a **Dependency Dashboard** (GitHub Issue).
3.  **Approval:** Updates are selected manually from the Dashboard to generate Pull Requests.
4.  **Deployment:** Merging a PR into `main` triggers the self-hosted GitHub Runner on the NAS to pull the new image and redeploy the container.

---

## ⚙️ Configuration Details

The logic is defined in `renovate.json5` at the root of the repository.

### Key Rules
* **Manual Approval:** Automerge is **disabled**. All updates require human review to ensure stability.
* **"Latest" Tag Management:**
    * If a container uses `image: plex:latest`, Renovate will create a PR to "pin" it to a specific digest (e.g., `plex:latest@sha256:...`).
    * This ensures immutable deployments—we always know *exactly* which version is running.
* **Database Safety:**
    * Major version updates for databases (Postgres, MariaDB, Mongo, Redis) are **blocked**.
    * *Reason:* Major DB upgrades often require manual data export/import and can corrupt data if done automatically.
* **Noise Reduction:**
    * Non-major updates (minor/patch) are grouped into single PRs where possible to reduce clutter.

### Settings Reference
| Setting | Value | Description |
| :--- | :--- | :--- |
| `dependencyDashboard` | `true` | Maintains a persistent "Master List" issue of all available updates. |
| `prHourlyLimit` | `0` (Unlimited) | Allows all PRs to be created immediately (bypassing spam filters). |

---

## 🚀 How to Process Updates

### 1. Check for Updates
* **Option A:** Look at the **Homarr Dashboard** on the NAS (via the GitHub widget).
* **Option B:** Go to the **Issues** tab in this repo and open the pinned issue titled **"Dependency Dashboard"**.

### 2. Approve & Trigger PRs
Renovate runs in "Interactive Mode." It finds updates but waits for permission to create the PR.
1.  Open the **Dependency Dashboard** issue.
2.  Tick the checkbox `[x]` next to the updates you want to apply.
3.  Wait for Renovate's next run (or trigger it manually via the Mend Dashboard).
4.  Renovate will generate a Pull Request for the selected items.

### 3. Review & Merge
1.  Go to the **Pull Requests** tab.
2.  Review the changelogs provided by Renovate.
3.  Click **Merge Pull Request**.
4.  ✅ **Done.** The NAS Runner picks up the change and deploys it automatically.
