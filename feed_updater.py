import os
import re
import logging
import asyncio
from datetime import datetime, timezone
from html import unescape
from typing import List, Optional

import aiohttp
import feedparser
from fastapi import FastAPI, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, HttpUrl
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

MONGO_URI = os.getenv("MONGO_URI")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_DEPLOYMENT_CHAT = os.getenv("AZURE_DEPLOYMENT_CHAT", "gpt-4o-mini")
AZURE_DEPLOYMENT_EMBED = os.getenv("AZURE_DEPLOYMENT_EMBED", "text-embedding-3-small")

SUMMARY_RETRY_ATTEMPTS = 3
SUMMARY_RATE_LIMIT_SECONDS = 20
SUMMARY_TIMEOUT = 30

# === MongoDB ===
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["rss_news_db"]
feeds_collection = db["rss_feeds"]
articles_collection = db["rss_articles"]
failed_collection = db["failed_summaries"]

# === Azure OpenAI ===
client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
)

# === FastAPI ===
app = FastAPI(
    title="RSS Feed Updater API",
    description="Manage feeds, fetch articles, and summarize with Azure OpenAI",
    version="2.0.0",
)

# === Pydantic Models ===
class FeedModel(BaseModel):
    source: str
    url: HttpUrl
    active: Optional[bool] = True

class ArticleModel(BaseModel):
    source: str
    title: str
    link: str
    published: datetime
    summary: str
    content: Optional[str]

# === Helpers ===
async def fetch_url(session, url):
    try:
        async with session.get(url, timeout=20) as resp:
            return await resp.text()
    except Exception as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None

def clean_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return unescape(text).strip()

async def get_embedding(text: str):
    try:
        response = client.embeddings.create(
            model=AZURE_DEPLOYMENT_EMBED,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        logging.error(f"Embedding failed: {e}")
        return []

async def safe_summary(content: str) -> str:
    prompt = f"Summarize the following news content in two sentences:\n\n{content}"

    for attempt in range(SUMMARY_RETRY_ATTEMPTS):
        try:
            response = client.chat.completions.create(
                model=AZURE_DEPLOYMENT_CHAT,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes news."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                timeout=SUMMARY_TIMEOUT,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if "429" in str(e):
                logging.warning(f"Rate limited, retrying in {SUMMARY_RATE_LIMIT_SECONDS}s...")
                await asyncio.sleep(SUMMARY_RATE_LIMIT_SECONDS)
            else:
                logging.error(f"Summary failed (attempt {attempt+1}): {e}")
                await asyncio.sleep(2)
    return ""

async def process_entry(entry, feed_source):
    title = clean_html(entry.get("title", ""))
    link = entry.get("link", "")
    published = datetime.now(timezone.utc)
    if "published_parsed" in entry and entry.published_parsed:
        published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

    description = clean_html(entry.get("summary", ""))
    content = clean_html(entry.get("content", [{}])[0].get("value", "")) or description

    if await articles_collection.find_one({"link": link}):
        return

    ai_summary = await safe_summary(content or description or title)
    if not ai_summary:
        await failed_collection.insert_one({
            "source": feed_source,
            "title": title,
            "link": link,
            "content": content,
            "timestamp": datetime.now(timezone.utc),
        })
        return

    embedding = await get_embedding(ai_summary)

    doc = {
        "source": feed_source,
        "title": title,
        "link": link,
        "published": published,
        "summary": ai_summary,
        "embedding": embedding,
        "content": content,
        "inserted_at": datetime.now(timezone.utc),
    }
    await articles_collection.insert_one(doc)
    logging.info(f"Inserted article: {title}")

async def update_feeds_once():
    async with aiohttp.ClientSession() as session:
        feeds = await feeds_collection.find({"active": True}).to_list(length=100)
        for feed in feeds:
            raw_data = await fetch_url(session, feed["url"])
            if not raw_data:
                continue
            parsed = feedparser.parse(raw_data)
            tasks = [process_entry(entry, feed["source"]) for entry in parsed.entries]
            await asyncio.gather(*tasks)

async def retry_failed_summaries():
    failed = await failed_collection.find().to_list(length=50)
    for doc in failed:
        ai_summary = await safe_summary(doc.get("content", ""))
        if ai_summary:
            embedding = await get_embedding(ai_summary)
            await articles_collection.insert_one({
                "source": doc["source"],
                "title": doc["title"],
                "link": doc["link"],
                "summary": ai_summary,
                "embedding": embedding,
                "content": doc.get("content", ""),
                "inserted_at": datetime.now(timezone.utc),
            })
            await failed_collection.delete_one({"_id": doc["_id"]})
            logging.info(f"Retried summary for {doc['title']}")

# === API Endpoints ===

@app.get("/feeds", response_model=List[FeedModel])
async def list_feeds():
    feeds = await feeds_collection.find().to_list(length=100)
    return feeds

@app.post("/feeds", response_model=FeedModel)
async def add_feed(feed: FeedModel):
    existing = await feeds_collection.find_one({"source": feed.source})
    if existing:
        raise HTTPException(status_code=400, detail="Feed source already exists")

    doc = feed.dict()
    doc["url"] = str(doc["url"])
    await feeds_collection.insert_one(doc)
    return feed

@app.put("/feeds/{source}", response_model=FeedModel)
async def update_feed(source: str, feed: FeedModel):
    result = await feeds_collection.update_one({"source": source}, {"$set": feed.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Feed not found")
    return feed

@app.delete("/feeds/{source}")
async def delete_feed(source: str):
    result = await feeds_collection.delete_one({"source": source})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Feed not found")
    return {"message": "Feed deleted"}

@app.post("/update-feeds")
async def update_feeds_endpoint():
    await update_feeds_once()
    return {"message": "Feeds updated successfully"}

@app.post("/retry-failed")
async def retry_failed_endpoint():
    await retry_failed_summaries()
    return {"message": "Failed summaries retried"}

@app.get("/articles", response_model=List[ArticleModel])
async def get_articles(limit: int = 10):
    cursor = articles_collection.find().sort("published", -1).limit(limit)
    return await cursor.to_list(length=limit)

@app.get("/search", response_model=List[ArticleModel])
async def search_articles(q: str = Query(..., min_length=3)):
    regex = {"$regex": q, "$options": "i"}
    cursor = articles_collection.find({"$or": [{"title": regex}, {"summary": regex}]}).limit(20)
    return await cursor.to_list(length=20)
