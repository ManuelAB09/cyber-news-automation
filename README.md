# Automated Cyber Threat Intel RSS Feed for Discord

An automated, serverless Python application that aggregates threat intelligence, vulnerability research, and security news from **17 high-quality cybersecurity RSS feeds** and posts them directly to a Discord channel using webhooks.

Powered by **GitHub Actions**, it runs fully in the cloud 24/7 with zero hosting costs, featuring intelligent HTML cleanup, multi-source rate limit handling, and isolated historical tracking per feed.

---

## Key Features

* **Automated Execution:** Runs hourly via GitHub Actions cron workflows (also supports manual triggers).
* **Rich Embed Layout:** Formats articles in an easily readable short preview format
* **Isolated Per-Source History:** Uses a structured JSON tracking system per feed (`MAX_HISTORY = 100` per source) to prevent fast-publishing feeds from purging history from slower sources, completely eliminating duplicate notifications.
* **Rate Limit Management:** Handles Discord's `HTTP 429 (Too Many Requests)` status natively by extracting `retry_after` headers and pausing execution safely.

---

## Included Threat Intelligence Feeds

The bot monitors 17 major cybersecurity blogs and vulnerability portals:

| Category | Sources |
| :--- | :--- |
| **News & Analysis** | Dark Reading, The Hacker News, Cyber Security News, BleepingComputer, The Register (Security), SecurityWeek, The Record |
| **Vendor & Threat Intel** | Huntress Blog, Microsoft Security, SOCRadar, Google Cloud Threat Intel, Cisco Talos, Rapid7, Okta Threat Intel, GreyNoise Intel |
| **Research & Advisory** | Krebs on Security, SANS Internet Storm Center (ISC) |

---

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── rss_bot.yml      # GitHub Actions workflow configuration
├── main.py                  # Primary Python script for parsing and sending RSS feeds
├── requirements.txt         # Python dependencies (feedparser, requests)
├── history.json             # Isolated historical cache (auto-updated by GitHub Actions)
└── README.md                # Project documentation
```

---

## Setup & Deployment Guide

### 1. Discord Webhook Setup
1. In your Discord server, go to **Server Settings > Integrations > Webhooks**.
2. Click **New Webhook**, select your target channel, and copy the **Webhook URL**.

### 2. Local Initialization & First Run
To prevent flooding Discord with historical posts on the first deployment, run the script locally to populate `history.json`:

1. Clone the repository and install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your environment variable and execute the script:
   
   **Linux/macOS:**
   ```bash
   export DISCORD_WEBHOOK_URL="your_discord_webhook_url"
   python main.py
   ```
   
   **Windows (PowerShell):**
   ```powershell
   $env:DISCORD_WEBHOOK_URL="your_discord_webhook_url"
   python main.py
   ```
3. Verify that `history.json` has been generated locally.

### 3. GitHub Repository & Secrets Configuration
1. Push all files (including `history.json` and `.github/`) to a private GitHub repository.
2. In your GitHub repository, navigate to **Settings > Secrets and variables > Actions**.
3. Click **New repository secret**.
4. Set **Name** to `DISCORD_WEBHOOK_URL` and paste your Discord Webhook URL into **Value**.
5. Save the secret.

---

## Configuration & Customization

* **Execution Schedule:** Edit `.github/workflows/rss_bot.yml` to change the cron schedule (default is hourly: `'0 * * * *'`).
* **Feed Limit per Run:** Edit `parsed_feed.entries[:50]` in `main.py` to adjust how many entries are processed per source during each check.
* **Source History Limit:** Edit `limit_per_source = 100` inside `save_history()` in `main.py` to change the tracking threshold.

---

## License

This project is open-source and available under the [MIT License](LICENSE).
