# Furry-Memes
(`furrymemes.com` & `furrymemes.net`)

# 🎯 Furry Memes Aggregator 

An automated content indexer, engagement scorer, and web frontend powering **[furrymemes.com](https://furrymemes.com)** (SFW) and **[furrymemes.net](https://furrymemes.net)** (NSFW 18+).

This project operates as an **artist-first search and discovery engine**. It queries public APIs across the web, scores content based on community engagement metrics, filters safe versus explicit content, and serves a high-performance JSON feed to a Next.js web application.

---

## 🛠️ Tech Stack & Architecture


```
┌────────────────────────────────────────────────────────────────────────┐
│                        Python Scraping Engine                          │
│     (Queries e926, e621, & Bluesky AppView APIs + Engagement Scorer)   │
└──────────────────────────────────┬─────────────────────────────────────┘
│
▼
┌───────────────────────┐
│  JSON Feed Output /   │
│   Supabase Database   │
└───────────┬───────────┘
│
┌─────────────────────────┴─────────────────────────┐
▼                                                   ▼
┌───────────────────────────────┐   ┌───────────────────────────────────┐
│     furrymemes.com (SFW)      │   │       furrymemes.net (NSFW)       │
│  - Mainstream Display Ads     │   │  - Client-side 18+ Cookie Gate    │
│  - SafeSearch Indexable       │   │  - Adult Network Monetization     │
│  - Top-of-Funnel SEO          │   │  - Explicit Content Rating Filter │
└───────────────────────────────┘   └───────────────────────────────────┘
```

* **Backend / Scraping:** Python 3.10+, `requests`, REST APIs (e926, e621, Bluesky AT Protocol)
* **Frontend:** Next.js (App Router), React, Tailwind CSS
* **Persistence & State:** JSON Feeds / Supabase, Client Cookie Management (Age Gate)

---

## 💡 Code & System Transparency

We believe in complete transparency regarding how content is discovered, evaluated, and displayed.

### 1. Data Sourcing & API Respect
* **No Unsanctioned Scraping:** The aggregator strictly utilizes official, public JSON/REST endpoints (e.g., e926, e621, and the public Bluesky AppView `searchPosts` endpoint).
* **User-Agent Integrity:** All requests sent to e621/e926 identify the application with an explicit, contactable `User-Agent` string in compliance with API terms of service.

### 2. Artist Attribution & Direct Link Policy
* **Source Links Preserved:** Every meme record ingested retains the original author's handle, post ID, and full permalink back to the source platform.
* **Direct Credit:** The UI prominently renders artist attribution badges (*"Art by @ArtistName on [Platform]"*) directing organic traffic straight back to the creator's official profile or post.

### 3. SFW / NSFW Filtering Logic
The python aggregator tags every piece of content with an `is_nsfw` flag and an explicit rating (`s` = safe, `q` = questionable, `e` = explicit):
* **`furrymemes.com`** serves strictly `rating: "s"` (`is_nsfw: false`) content to maintain search engine compliance and high-CPM ad safety.
* **`furrymemes.net`** serves all content tiers (`s`, `q`, `e`) behind a mandatory, cookie-persisted 18+ Age Gate.

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* Node.js 18+ & `npm` / `pnpm`

### 1. Running the Scraper

```bash
# Clone the repository
git clone [https://github.com/your-username/furry-memes-aggregator.git](https://github.com/your-username/furry-memes-aggregator.git)
cd furry-memes-aggregator

# Install Python dependencies
pip install -r requirements.txt

# Run the NSFW-friendly scraper (generates furry_memes_nsfw.json)
python scrapers/fetch_memes_nsfw.py

```
### 2. Running the Web Frontend
```bash
# Install frontend packages
npm install

# Run development server
npm run dev

```
Open http://localhost:3000 with your browser to see the output.
## ⚖️ Content & Copyright Notice
This repository functions solely as an indexing and curation tool. All artwork, images, and characters remain the intellectual property of their respective creators.
If you are an artist and wish to have your content excluded from our indexing engine, please submit a request or open an issue in this repository with your artist handle, and your content will be added to our global blacklist.
## 📜 License
Distributed under the MIT License. See LICENSE for more information.

```
https://BUNREC.com mailto:XObunrec@gmail.com © 2026
```
