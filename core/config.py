from dotenv import load_dotenv
import os

load_dotenv()

STRAVA_CONFIG = {
    "url": "https://www.strava.com",
    "creds": {"user": os.getenv("STRAVA_USER"), "psw": os.getenv("STRAVA_PSW")},
}



