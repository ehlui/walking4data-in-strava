from requests import utils as request_utils
from pathlib import Path
import requests
import json
from core.utils.helpers import create_dir_if_not_exists


def persist_cookies(ck_path: str, ck_name: str, session: requests.Session):
    """To avoid being block we need to use the session"""
    cookies_dict = request_utils.dict_from_cookiejar(cj=session.cookies)

    if ck_path is None:
        return

    print("---- saving strava cookies ---")
    create_dir_if_not_exists(dirpath=ck_path)
    Path(f"{ck_path}{ck_name}").write_text(json.dumps(cookies_dict))


def load_cookies(ck_path, ck_name, session: requests.Session) -> bool:
    if ck_path is None:
        return False

    cookies_path = Path(f"{ck_path}{ck_name}")

    if not cookies_path.exists():
        print(f"Cookies not found in <'{ck_path}{ck_name}'>")
        return False

    cookies = json.loads(cookies_path.read_text())
    cookies = request_utils.cookiejar_from_dict(cookie_dict=cookies)
    session.cookies.update(cookies)
    return True
