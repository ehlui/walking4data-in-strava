import core.config as config
import time
import random
from bs4 import BeautifulSoup
import os


def get_base_url() -> str:
    return config.STRAVA_CONFIG["url"]


def do_rnd_sleep(sleeping_seconds_range: tuple[int]) -> None:
    time.sleep(random.randint(*sleeping_seconds_range))


def fetch_html_parsed(url: str, session, headers, sleep_range=(2, 8)) -> BeautifulSoup:
    """Class only method for extracting user HTML parsed by our friendly bs4"""

    if url is None:
        return

    do_rnd_sleep(sleep_range)

    resp = session.get(url=url, headers=headers)

    # print(f"fetching html from <{url}> :: status-code <{resp.status_code}>")

    return BeautifulSoup(resp.text, "lxml")


def create_dir_if_not_exists(dirpath: str):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
