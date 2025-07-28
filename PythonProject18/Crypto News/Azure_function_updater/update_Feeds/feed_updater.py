import asyncio
import logging
from datetime import datetime, timezone
import os

import feedparser
from motor.motor_asyncio import AsyncIOMotorClient
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
print("DEBUG OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
cd 

MONGO_URI = os.getenv("MONGO_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not MONGO_URI:
    logging.error("MONGO_URI not set!")
if not OPENAI_API_KEY:
    logging.error("OPENAI_API_KEY not set!")

feedparser.USER_AGENT = "Mozilla/5.0 (compatible; AzureFeedUpdater/1.0)"

RSS_FEEDS = {
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "99bitcoins": "https://99bitcoins.com/feed/",
    "Decrypt": "https://decrypt.co/feed",
    "Cointelegraph": "https://cointelegraph.com/rss",
    "NFTLately": "https://nftlately.com/feed/"
}

# Mongo
mongo_client = AsyncIOMotorClient(MONGO_URI) if MONGO_URI else None
db = mongo_client["rss_news_db"] if mongo_client else None
collection = db["summaries"] if db is not None else None

# OpenAI (LangChain)
prompt = PromptTemplate(
    input_variables=["summary"],
    template="Summarize news content in two sentences: {summary}"
)
llm = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
summarizer_chain = prompt | llm


async def safe_summary(summary_text: str, timeout: int = 30) -> str:
    try:
        resp = await asyncio.wait_for(
            summarizer_chain.ainvoke({"summary": summary_text[:1000]}),
            timeout
        )
        return resp.content if hasattr(resp, "content") else str(resp)
    except Exception:
        logging.exception("AI summarization failed")
        return "summary failed"


async def parse_feed_async(url: str):
    try:
        return await asyncio.to_thread(feedparser.parse, url)
    except Exception:
        logging.exception("Failed to parse feed: %s", url)
        return None


async def process_entry(entry, source: str) -> bool:
    try:
        if not collection:
            logging.error("Mongo collection is not initialized.")
            return False

        if await collection.find_one({"link": entry.link}):
            return False  # already exists

        raw_summary = entry.get("summary", entry.get("title", ""))[:1000]
        ai_summary = await safe_summary(raw_summary)

        article = {
            "title": entry.title,
            "link": entry.link,
            "published": entry.get("published", "N/A"),
            "source": source,
            "original_summary": raw_summary,
            "ai_summary": ai_summary,
            "created_at": datetime.now(timezone.utc)
        }

        await collection.insert_one(article)
        return True
    except Exception:
        logging.exception("Failed processing entry from %s", source)
        return False


async def update_feeds_once(limit_per_feed: int = 10):
    inserted, skipped = 0, 0
    for source, url in RSS_FEEDS.items():
        feed = await parse_feed_async(url)
        if not feed or not getattr(feed, "entries", None):
            logging.warning("No entries for %s", source)
            continue

        for entry in feed.entries[:limit_per_feed]:
            ok = await process_entry(entry, source)
            if ok:
                inserted += 1
            else:
                skipped += 1
    logging.info("Update finished. Inserted=%s, Skipped=%s", inserted, skipped)


def run_update():
    try:
        asyncio.run(update_feeds_once())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(update_feeds_once())
