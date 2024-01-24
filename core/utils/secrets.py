import base64
from core.config import STRAVA_CONFIG


def read_creds() -> list[str]:
    return [
        STRAVA_CONFIG["creds"]["user"],
        decode_psw(STRAVA_CONFIG["creds"]["psw"])
    ]

def decode_psw(psw: str):
    return base64.b64decode(psw).decode('utf-8')