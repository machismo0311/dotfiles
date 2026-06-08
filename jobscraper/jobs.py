import urllib.request
import xml.etree.ElementTree as ET
import json
from datetime import datetime

def fetch_remoteok():
    url = "https://remoteok.com/api"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode())
        jobs = []
        for j in data[1:]:
            tags = " ".join(j.get("tags", [])).lower()
            title = j.get("position", "").lower()
            if any(k in tags or k in title for k in ["operations", "aviation", "project", "management", "consulting", "coordinator"]):
                jobs.append({
                    "title": j.get("position", ""),
                    "company": j.get("company", ""),
                    "link": j.get("url", ""),
                    "date": j.get("date", "")
                })
        return jobs[:20]
    except Exception as e:
        print(f"RemoteOK error: {e}")
        return []

def fetch_wwr():
    url = "https://weworkremotely.com/categories/remote-management-and-finance-jobs.rss"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            tree = ET.parse(r)
        root = tree.getroot()
        channel = root.find("channel")
        jobs = []
        for item in channel.findall("item"):
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            date = item.findtext("pubDate", "").strip()
            jobs.append({"title": title, "company": "", "link": link, "date": date})
        return jobs[:20]
    except Exception as e:
        print(f"WWR error: {e}")
        return []

def build_html(remoteok_jobs, wwr_jobs):
    now = datetime.now().strftime("%B %d, %Y %I:%M %p")

    def make_cards(jobs):
        if not jobs:
            return "<p class='none'>No results found.</p>"
        cards = ""
        for j in jobs:
            cards += f"""
            <a href="{j['link']}" target="_blank" class="card">
                <div class="title">{j['title']}</div>
                <div class="meta">{j['company']}</div>
                <div class="date">{j['date']}</div>
            </a>"""
        return f"<div class='grid'>{cards}</div>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Remote Jobs</title>
<style>
  body {{ font-family: Georgia, serif; background: #0a0a0a; color: #fff; padding: 3rem 2rem; max-width: 900px; margin: 0 auto; }}
  h1 {{ font-weight: 300; letter-spacing: 0.2em; text-transform: uppercase; font-size: 1.5rem; margin-bottom: 0.5rem; }}
  .updated {{ color: rgba(255,255,255,0.35); font-size: 0.75rem; margin-bottom: 3rem; letter-spacing: 0.1em; }}
  h2 {{ font-weight: 300; font-size: 1rem; letter-spacing: 0.15em; text-transform: uppercase; color: rgba(255,255,255,0.5); margin: 2.5rem 0 1rem; border-bottom: 0.5px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem; }}
  .grid {{ display: flex; flex-direction: column; gap: 1rem; }}
  .card {{ display: block; text-decoration: none; color: inherit; background: rgba(255,255,255,0.04); border: 0.5px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 1rem 1.25rem; transition: background 0.2s; }}
  .card:hover {{ background: rgba(255,255,255,0.08); }}
  .title {{ font-size: 1rem; margin-bottom: 0.35rem; }}
  .meta {{ font-size: 0.8rem; color: rgba(255,255,255,0.45); }}
  .date {{ font-size: 0.7rem; color: rgba(255,255,255,0.25); margin-top: 0.35rem; }}
  .none {{ color: rgba(255,255,255,0.3); font-size: 0.85rem; }}
</style>
</head>
<body>
<h1>Remote Jobs</h1>
<p class="updated">Updated {now}</p>
<h2>Remote OK — Operations & Management</h2>
{make_cards(remoteok_jobs)}
<h2>We Work Remotely — Management & Finance</h2>
{make_cards(wwr_jobs)}
</body>
</html>"""

print("Fetching RemoteOK...")
remoteok_jobs = fetch_remoteok()
print(f"Found {len(remoteok_jobs)} jobs on RemoteOK")

print("Fetching We Work Remotely...")
wwr_jobs = fetch_wwr()
print(f"Found {len(wwr_jobs)} jobs on WWR")

html = build_html(remoteok_jobs, wwr_jobs)
with open("jobs.html", "w") as f:
    f.write(html)
print("Done — open jobs.html in your browser")
