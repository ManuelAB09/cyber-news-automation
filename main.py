import feedparser
import requests
import json
import os
import re
import time
import html
from datetime import datetime, timezone

WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
HISTORY_FILE = 'history.json'
MAX_HISTORY_SIZE = 1000

FEEDS = {
    "Dark Reading": "https://www.darkreading.com/rss.xml",
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "Huntress Blog": "https://www.huntress.com/blog/rss.xml",
    "Microsoft Security": "https://www.microsoft.com/en-us/security/blog/feed/",
    "Cyber Security News": "https://cybersecuritynews.com/feed/",
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    "SOCRadar": "https://socradar.io/feed/",
    "Krebs on Security": "https://krebsonsecurity.com/feed/",
    "SANS ISC": "https://isc.sans.edu/rssfeed_full.xml",
    "The Register (Security)": "https://www.theregister.com/security/headlines.atom",
    "The Record": "https://therecord.media/feed/",
    "SecurityWeek": "https://www.securityweek.com/feed/",
    "Google Cloud Threat Intel": "https://cloudblog.withgoogle.com/topics/threat-intelligence/rss/",
    "Cisco Talos": "https://blog.talosintelligence.com/rss/",
    "Rapid7": "https://blog.rapid7.com/rss/",
    "Okta Threat Intel": "https://www.okta.com/blog/threat-intelligence.rss",
    "Grey Noise": "https://www.greynoise.io/blog/rss.xml"
}

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return {}
            return data
    return {}

def save_history(history):
    limit_per_source = 100
    for source in history:
        if len(history[source]) > limit_per_source:
            history[source] = history[source][-limit_per_source:]
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def clean_html(raw_html):
    clean_text = html.unescape(raw_html)
    clean_text = re.sub(r'<[^>]+>', '', clean_text).strip()
    clean_text = clean_text.replace('&nbsp;', ' ')
    clean_text = re.sub(r'\n+', ' ', clean_text)
    if len(clean_text) > 300:
        return clean_text[:297] + "..."
    return clean_text

def send_to_discord(entry, source_name):
    title = entry.get('title', 'New Article')
    link = entry.get('link', '')
    description = ""
    
    if 'summary' in entry:
        description = clean_html(entry.summary)
        
    image_url = ""
    if 'media_content' in entry and len(entry.media_content) > 0:
        image_url = entry.media_content[0].get('url', '')
    elif 'media_thumbnail' in entry and len(entry.media_thumbnail) > 0:
        image_url = entry.media_thumbnail[0].get('url', '')
    elif 'links' in entry:
        for l in entry.links:
            if 'image' in l.get('type', ''):
                image_url = l.get('href', '')
                break

    author = entry.get('author', '')
    tags = ""
    if 'tags' in entry:
        tag_list = [tag.get('term') for tag in entry.tags if tag.get('term')]
        if tag_list:
            tags = " | ".join(tag_list[:3])

    embed = {
        "title": title,
        "url": link,
        "description": description,
        "color": 15158332, 
        "footer": {
            "text": f"Source: {source_name}"
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    if image_url:
        embed["thumbnail"] = {"url": image_url} 
        
    if author:
        embed["author"] = {"name": f"Author: {author}"}
        
    if tags:
        embed["fields"] = [
            {
                "name": "Tags",
                "value": tags,
                "inline": True
            }
        ]

    data = {"embeds": [embed]}
    max_retries = 3
    
    for attempt in range(max_retries):
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print(f"[OK] Sent: {title} ({source_name})")
            time.sleep(1)
            return True
        elif response.status_code == 429:
            try:
                error_data = response.json()
                wait_time = error_data.get('retry_after', 2.0)
            except Exception:
                wait_time = 2.0
            print(f"[RATE LIMIT] HTTP 429. Sleeping for {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            print(f"[ERROR] Failed to send '{title}'. HTTP {response.status_code}")
            return False
    return False

def main():
    if not WEBHOOK_URL:
        print("[CRITICAL] DISCORD_WEBHOOK_URL environment variable is missing.")
        return

    history = load_history()
    new_urls = []

    for source_name, feed_url in FEEDS.items():
        print(f"Fetching: {source_name}...")
        if source_name not in history:
            history[source_name] = []
            
        try:
            parsed_feed = feedparser.parse(feed_url)
        except Exception as e:
            print(f"[ERROR] Failed to fetch {source_name}: {e}")
            continue
        
        for entry in reversed(parsed_feed.entries[:50]):
            link = entry.get('link')
            if link and link not in history[source_name]:
                success = send_to_discord(entry, source_name)
                if success:
                    history[source_name].append(link)
                    new_urls.append(link)
                
    if new_urls:
        save_history(history)
        print(f"[SUCCESS] Sent {len(new_urls)} new articles.")
    else:
        print("[INFO] No new articles found.")

if __name__ == "__main__":
    main()