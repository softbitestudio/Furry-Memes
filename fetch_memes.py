from datetime import datetime, timezone
import json
import logging
import re
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Note: e926 mandates a descriptive User-Agent with contact info.
HEADERS = {
    "User-Agent": "FurryMemesAggregator/1.0 (contact: admin@furrymemes.com)"
}

def fetch_e926_memes(min_score=15, limit=30):
    """
    Fetches SFW memes from e926.net matching tag & minimum score criteria.
    """
    url = "https://e926.net/posts.json"
    params = {
        "tags": f"meme score:>={min_score}",
        "limit": limit
    }
    
    memes = []
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        for post in data.get("posts", []):
            # Verify file exists and is an image/gif
            file_info = post.get("file", {})
            file_url = file_info.get("url")
            ext = file_info.get("ext")
            
            if not file_url or ext in ["webm", "swf"]:
                continue
                
            artist_list = post.get("tags", {}).get("artist", [])
            artist = artist_list[0] if artist_list else "Unknown Artist"
            
            score = post.get("score", {}).get("total", 0)
            post_id = post.get("id")
            
            memes.append({
                "id": f"e926_{post_id}",
                "source": "e926",
                "title": f"Meme by {artist}",
                "caption": ", ".join(post.get("tags", {}).get("general", [])[:5]),
                "image_url": file_url,
                "preview_url": post.get("preview", {}).get("url") or file_url,
                "source_url": f"https://e926.net/posts/{post_id}",
                "artist_handle": artist,
                "created_at": post.get("created_at"),
                "raw_metrics": {"score": score},
                # Normalize e926 upvotes to a standard score
                "engagement_score": round(score * 1.5, 2)
            })
            
        logging.info(f"Fetched {len(memes)} memes from e926.")
    except Exception as e:
        logging.error(f"Error fetching from e926: {e}")
        
    return memes

def extract_bsky_images(embed):
    """
    Helper to extract image URLs from Bluesky embed structures.
    """
    if not embed:
        return []
    
    embed_type = embed.get("$type", "")
    images = []
    
    if "app.bsky.embed.images" in embed_type:
        images = embed.get("images", [])
    elif "app.bsky.embed.recordWithMedia" in embed_type:
        media = embed.get("media", {})
        if "app.bsky.embed.images" in media.get("$type", ""):
            images = media.get("images", [])
            
    return [img.get("fullsize") or img.get("thumb") for img in images if img.get("fullsize") or img.get("thumb")]

def fetch_bluesky_memes(query="furry meme", limit=30):
    """
    Fetches public posts matching query from Bluesky using public AppView endpoint.
    """
    url = "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts"
    params = {
        "q": query,
        "sort": "top",
        "limit": limit
    }
    
    memes = []
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        for post in data.get("posts", []):
            author = post.get("author", {})
            record = post.get("record", {})
            embed = post.get("embed", {})
            
            images = extract_bsky_images(embed)
            if not images:
                continue  # Skip text-only posts
                
            likes = post.get("likeCount", 0)
            reposts = post.get("repostCount", 0)
            
            # Construct web permalink
            uri = post.get("uri", "")
            rkey = uri.split("/")[-1] if "/" in uri else ""
            handle = author.get("handle", "user")
            permalink = f"https://bsky.app/profile/{handle}/post/{rkey}" if rkey else ""
            
            memes.append({
                "id": f"bsky_{rkey}",
                "source": "bluesky",
                "title": f"Post by @{handle}",
                "caption": record.get("text", "").strip(),
                "image_url": images[0],  # Primary image
                "preview_url": images[0],
                "source_url": permalink,
                "artist_handle": author.get("displayName") or handle,
                "created_at": record.get("createdAt"),
                "raw_metrics": {"likes": likes, "reposts": reposts},
                # Bluesky weight formula: 1 like = 1 pt, 1 repost = 2.5 pts
                "engagement_score": round(likes + (reposts * 2.5), 2)
            })
            
        logging.info(f"Fetched {len(memes)} memes from Bluesky.")
    except Exception as e:
        logging.error(f"Error fetching from Bluesky: {e}")
        
    return memes

def generate_meme_feed(output_file="furry_memes_feed.json"):
    """
    Aggregates, deduplicates, sorts by score, and saves output JSON.
    """
    all_memes = []
    
    # 1. Gather from sources
    all_memes.extend(fetch_e926_memes(min_score=10, limit=30))
    all_memes.extend(fetch_bluesky_memes(query="furry meme", limit=30))
    all_memes.extend(fetch_bluesky_memes(query="#furrymeme", limit=30))
    
    # 2. Deduplicate by image URL or ID
    seen_ids = set()
    deduped_memes = []
    for item in all_memes:
        if item["id"] not in seen_ids and item["image_url"]:
            seen_ids.add(item["id"])
            deduped_memes.append(item)
            
    # 3. Sort by engagement score descending
    deduped_memes.sort(key=lambda x: x["engagement_score"], reverse=True)
    
    # 4. Wrap into final feed structure
    feed_payload = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_count": len(deduped_memes),
            "sources": ["e926", "bluesky"]
        },
        "memes": deduped_memes
    }
    
    # 5. Export to file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(feed_payload, f, indent=2, ensure_ascii=False)
        
    logging.info(f"Successfully generated {output_file} with {len(deduped_memes)} memes.")

if __name__ == "__main__":
    generate_meme_feed()
