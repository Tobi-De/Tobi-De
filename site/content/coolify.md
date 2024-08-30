# Coolify

Here's an improved version of your text, keeping the original tone:

@adamghill@indieweb.social
Have you ever tried Coolify (especially recently)?
I tried it a while ago, but I was already using CapRover, and my impressions were basically "meh, nothing interesting here."
But I watched the latest Fireship video and decided to give it another try yesterday, and oh boy 😬 it does everything CapRover does plus some more. The main highlights for me:
- Easily add a job via the UI to automatically backup PostgreSQL databases (but I don't think it uses pg_dump or something similar, just backs up the whole container, I think. Not sure how the AWS S3 costs will go with this)
- Run a command on the server or in a container from the UI. It's not interactive (that's something that has always frustrated me with CapRover)
- Stop a service from the UI. Never thought I needed this until a few weeks ago
- Stop the proxy service that comes with it (Traefik by default, but can be switched to Caddy or Nginx) so that I can easily keep control of my 80 and 443 ports if needed
I'm probably going with it for future deployments, but probably not really for Django. I'm trying to optimize and automate a lot of my classic VPS workflow (systemd, Gunicorn, Nginx) with Justfile and keeping the config files in my repos.