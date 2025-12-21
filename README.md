GitOps Migration Status

I am migrating a massive chunk of my NAS infrastructure to GitOps. My Gdive folder on my MacBook now holds the "Source of Truth" and then synched up to Github for:

✅ Media: Plex, Emby, Audiobookshelf, Booklore

✅ Core: Pi-hole, Tailscale, Homarr, Duplicati

✅ Heavy Lifters: Immich, Frigate, OpenArchiver

This is a huge achievement. If my NAS exploded tomorrow I could buy a new one, install Portainer, plug in your hard drives, and run docker compose up on your GitHub repo to restore your entire digital life in minutes!!! Woop!

GitOps Health Checks
Now that you have successfully migrated everything to GitOps, your infrastructure is in a very advanced state. Before you relax, let's run a 3-point health check to ensure this new system is bulletproof.

1. The "Reboot" Test (Simulation)
You don't need to actually reboot the NAS, but you should verify that your containers will survive one.

Action: Pick a non-critical stack (like audiobookshelf).
Test: Delete the container in Portainer (Simulating a crash).
Result: It should disappear.
Recovery: Click "Pull and redeploy" in the Stack.
Verification: Audibookshelf container ame back with all your books and progress saved, so my Volume mappings and other yaml is good

2. The "GitOps" Test (The GitHub Loop)
Verify that your "Control Center" on the Mac is working.

Action: On your Mac, edit watchtower/docker-compose.yml. Change WATCHTOWER_SCHEDULE slightly (e.g., to 0 0 */24 * * *).
Command: git add . then git commit -m "Test change" then git push.
Action: Go to Portainer -> Watchtower Stack -> Click "Pull and redeploy".
Verification: Checked the container logs and the schedule did change so all good

3. The "Communication" Test (DNS)
Since you moved to GitOps, Docker creates new internal networks for each stack. We need to ensure containers can still talk to each other (e.g., Homarr talking to Plex).

Action: Open Homarr.

Test: Do the "Ping" dots for your services (Plex, Sonarr, etc.) show as Green?

Troubleshooting: If they are Red, it's likely because they are now on different Docker networks.

Quick Fix: If internal DNS fails, you might need to use the NAS IP (192.168.68.XXX) instead of the container name (plex) inside Homarr's settings, OR add them all to a shared external network in your Compose files.

You have done an incredible job today. You went from a standard setup to a fully version-controlled, secure, automated GitOps infrastructure. Your NAS is now ready for anything.

Getting "Green across the board" on a migration this complex—involving Macvlan, Tailscale kernel drivers, and the full Immich stack—is a serious achievement.

You have effectively moved your home infrastructure from "Hobbyist" level to "Enterprise/SRE" level. Your NAS is now resilient, portable, and version-controlled.

Before we close this off, here is your "Day 2 Operations" Cheat Sheet. Save this somewhere; it is the summary of the new rules for managing your server.

📜 The New Golden Rules
1. The Source of Truth is GitHub

Never change volumes, ports, or image tags inside the Portainer UI.

Always edit the YAML on your MacBook (nas-stacks), commit, and push.

Why? If you edit in Portainer, the next time you redeploy from Git, your manual changes will be wiped out.

2. The Secrets Vault is Portainer

Never put passwords in the YAML file on your Mac.

Always use ${VARIABLE_NAME} in the YAML and define the value in the Portainer Stack settings.

3. The Update Workflow

Config Change: Edit Mac -> git push -> Portainer "Pull and redeploy".

Software Update (Watchtower): You set Watchtower to run every 12 hours. It will auto-update any container using the :latest tag (like Plex and Homarr). You don't need to do anything.

⚠️ One Final Technical "Gotcha" (Watchtower vs. GitOps)
Since you are using Watchtower alongside GitOps, there is one small nuance to remember:

Scenario: You defined image: pihole:latest in GitHub. Watchtower sees a new version and updates the container on your NAS automatically. Great.

The Gotcha: If you defined a specific version in GitHub (e.g., image: frigate:0.14.0) and Watchtower forcibly updates it to 0.15.0, your system is now "Drifting." The next time you click "Pull and redeploy" in Portainer, it will read GitHub (0.14.0) and downgrade you back to the old version.

The Fix: If you want Watchtower to handle updates, ensure your GitHub YAML uses dynamic tags like :latest, :stable, or :release (which you did for Immich). If you pin a specific version number, you must update that number in GitHub manually to "lock in" the upgrade.

Quick Summary of what I have built in terms of Doom server:

Hardware: Synology NAS (Intel N100) running Docker.
Software: Portainer managing a custom stack.
Network: 4 distinct UDP ports forwarded and firewall-approved.
Capabilities: Simultaneous hosting of vanilla 1993 Doom (Chocolate) and modern modded Doom/Hexen (Zandronum) with a client-side menu system.
