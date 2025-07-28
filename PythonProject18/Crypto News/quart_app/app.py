from quart import Quart, render_template
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

app = Quart(__name__)


mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["rss_news_db"]
collection = db["summaries"]

@app.route('/')
async def home():
    articles_cursor = collection.find().sort("created_at", -1).limit(10)
    articles = await articles_cursor.to_list(length=10)
    return await render_template("index.html", articles=articles)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
