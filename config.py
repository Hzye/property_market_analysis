import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SCRAPE_URL = os.getenv("SCRAPE_URL")
    MONGO_URI = os.getenv("MONGO_URL")

    APP_TITLE = "🏠 Australian Property Market Analysis"
    HOME_TITLE = "Home"

    # Theme and styling
    THEME_PRIMARY_COLOR = "#4b78e6"
    THEME_SECONDARY_COLOR = "#f0f2f6"
    THEME_TEXT_COLOR = "#262730"
