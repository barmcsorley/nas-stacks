# 🏠 Home Lab GitOps Documentation

This repository hosts the Infrastructure-as-Code (IaC) configuration for the Home Lab running on the UGreen NAS. We utilize a **GitOps** model, meaning the state of the repository acts as the "Source of Truth" for the infrastructure.

## 🏗 Hardware & Environment

* **Server:** UGreen 2800DXP NAS
* **OS/Hypervisor:** UGOS Pro (Docker/Container Manager)
* **Storage Path:** `/volume2/FastSSD/docker`
* **Orchestration:** Docker Compose (managed via GitOps)

## 🔄 The GitOps Workflow

We do not manually update containers using Portainer or Watchtower. Instead, we use an automated pipeline:

1.  **Detection:** [Renovate](https://www.mend.io/renovate/) scans this repository hourly.
2.  **Reporting:** Updates are listed in the **Dependency Dashboard** (GitHub Issue).
3.  **Approval:** A human ticks a checkbox in the Dashboard to request an update.
4.  **Pull Request:** Renovate creates a PR with release notes.
5.  **Deployment:** When the PR is merged, a **Self-Hosted GitHub Runner** on the NAS pulls the changes and redeploys the specific stack.

---

## 📂 Repository Structure

Each application stack resides in its own directory containing its specific configuration.

```text
nas-stacks/
├── .github/
│   └── workflows/          # CI/CD Pipelines (deploy.yml)
├── renovate.json5          # Update bot configuration
├── .env.example            # Template for environment variables
├── README.md               # This documentation
├── plex/
│   └── docker-compose.yml  # Stack definition
├── radarr/
│   └── docker-compose.yml
└── ...
