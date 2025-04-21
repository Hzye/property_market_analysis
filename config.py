import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SCRAPE_URL = os.getenv("SCRAPE_URL")
    MONGO_URI = os.getenv("MONGO_URL")

    APP_TITLE = "🏠 Australian Property Market Analysis"