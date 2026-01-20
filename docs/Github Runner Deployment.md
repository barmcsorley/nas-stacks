# 🚀 Automated Deployment Strategy (GitHub Runner)

This repository uses a **Self-Hosted GitHub Runner** installed directly on the UGreen NAS to handle Continuous Deployment (CD). When a Pull Request is merged, this runner executes the changes locally on the server.

## 🏗 Architecture

| Component | Role | Location |
| :--- | :--- | :--- |
| **GitHub Actions** | Orchestrator | Cloud (GitHub.com) |
| **Self-Hosted Runner** | Executor | UGreen NAS (`/volume2/FastSSD/docker`) |
| **Deployment Workflow** | Logic Script | `.github/workflows/deploy.yml` |

## ⚙️ How It Works

1.  **Trigger:** A Pull Request (from Renovate or a human) is merged into the `main` branch.
2.  **Pickup:** GitHub queues a job. The Runner on the NAS (listening for jobs with the tag `self-hosted` or similar) claims it.
3.  **Execution:**
    * The Runner checks out the latest code from `main`.
    * It identifies which `docker-compose.yaml` files have changed.
    * It runs `docker compose pull` and `docker compose up -d` for the specific stack.
4.  **Result:** The container is recreated with the new image tag, preserving all existing volumes and configuration.

## 🛠 Runner Maintenance

The Runner itself runs as a service/container on the NAS.

### Checking Status
You can verify the runner is online by going to:
**GitHub Repository** -> **Settings** -> **Actions** -> **Runners**.
* 🟢 **Idle:** Ready to take jobs.
* ⚪ **Offline:** Needs a restart.

### Troubleshooting Failed Deployments
If a deployment fails (Red X in GitHub Actions tab):
1.  **Check the Logs:** Click the failed run in the "Actions" tab on GitHub. The logs stream directly from the NAS.
2.  **Common Errors:**
    * *Permission Denied:* The runner cannot read the `docker-compose.yaml`. Ensure the runner user has `rw` permissions on the docker folder.
    * *Docker Socket:* The runner cannot talk to the Docker daemon. Ensure the volume mount `/var/run/docker.sock:/var/run/docker.sock` is active.

## 🔐 Security Note
This runner has direct access to the NAS Docker socket.
* **Repo Access:** Ensure only trusted users have "Write" access to this repository.
* **Secrets:** Sensitive environment variables (API Keys) are stored in **GitHub Secrets** and injected into the `.env` file during deployment, or managed locally on the NAS.
