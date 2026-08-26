# 🛡️ Automated Cyber Threat Intel RSS Feed for Discord

An automated, serverless Python application that aggregates threat intelligence, vulnerability research, and security news from **17 high-quality cybersecurity RSS feeds** and posts them directly to a Discord channel using webhooks.

Powered by **GitHub Actions**, it runs fully in the cloud 24/7 with zero hosting costs, featuring intelligent HTML cleanup, multi-source rate limit handling, and isolated historical tracking per feed.

---

## Key Features

* **Automated Execution:** Runs hourly via GitHub Actions cron workflows (also supports manual triggers).
* **Rich Embed Layout:** Formats articles with easily readable short preview of the news in the channel.
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

##  Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── rss_bot.yml      # GitHub Actions workflow configuration
├── main.py                  # Primary Python script for parsing and sending RSS feeds
├── requirements.txt        # Python dependencies (feedparser, requests)
├── history.json             # Isolated historical cache (auto-updated by GitHub Actions)
└── README.md                # Project documentation
