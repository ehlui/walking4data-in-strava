from core.cookiehandler import load_cookies, persist_cookies
from core.utils.helpers import get_base_url, do_rnd_sleep
from core.utils.secrets import read_creds

from bs4 import BeautifulSoup
from core import requestheaders
import requests


class StravaSession:
    sleeping_seconds_range = (3, 15)
    login_selectors = {
        "authenticity_token": "#login_form > input[type=hidden]:nth-child(2)"
    }
    avatar_oboarding_sel = "img.avatar-img"
    user_selector = "div.athlete-name"

    is_logged = False
    session: requests.Session

    def __init__(self) -> None:
        self.cookies_defualt_path = "core/cookies/"
        self.cookies_name = "strava_cookies.json"
        self.base_url = get_base_url()
        self.session_url = f"{self.base_url}/session"
        self.dashboard_url = f"{self.base_url}/dashboard"
        self.onboardig_url = f"{self.base_url}/onboarding"
        self.session = requests.Session()

    def __go_to_login_page_w_session(self):
        url = f"{self.base_url}/login"
        s = self.session.get(url=url, headers=requestheaders.headers.get("to_login"))
        return BeautifulSoup(s.text, "lxml")

    def __build_loggin_payload(self):
        creds = read_creds()
        return {
            "utf8": "✓",
            "email": creds[0],
            "password": creds[1],
            "remember_me": "on",
            "plan": "",
        }

    def __do_login(self, auth_token):
        data = self.__build_loggin_payload()
        data.update(auth_token)

        requestheaders.headers["Location"] = self.dashboard_url

        response_session = self.session.post(
            url=self.session_url,
            data=data,
            headers=requestheaders.headers.get("to_login"),
            allow_redirects=False,
        )

        #status_code_response = response_session.status_code
        #print(f"/login => {status_code_response}")

    def start(self, do_persists_cookies: bool = True):
        """Inizialize the session creation.
        If there is a session stored it will used,
        else it will created making the logging"""

        are_loaded = load_cookies(
            ck_path=self.cookies_defualt_path,
            ck_name=self.cookies_name,
            session=self.session,
        )

        if are_loaded:
            print("--- Using loaded cookes ---")
            return

        soup = self.__go_to_login_page_w_session()

        authenticity_token_tag = soup.select_one(
            self.login_selectors["authenticity_token"]
        )
        authenticity_token_name = authenticity_token_tag.attrs.get("name")
        authenticity_token_value = authenticity_token_tag.attrs.get("value")

        # self.do_sleep()
        do_rnd_sleep(self.sleeping_seconds_range)

        self.__do_login(auth_token={authenticity_token_name: authenticity_token_value})

        if do_persists_cookies:
            persist_cookies(
                ck_path=self.cookies_defualt_path,
                ck_name=self.cookies_name,
                session=self.session,
            )

    def is_log_in_ok(self):
        """
        Most of GET request are 200,
        so a way to check whether we are in is to check our profile right after logging in
        """

        if self.is_logged:
            return True

        do_rnd_sleep(self.sleeping_seconds_range)

        resp = self.session.get(
            headers=requestheaders.headers.get("on_login"), url=self.onboardig_url
        )

        soup = BeautifulSoup(resp.text, "lxml")

        # user_name_tag = soup.select_one(self.user_selector)
        # if user_name_tag is not None:
        #    print(f"--- Logged as <{user_name_tag.text}> in strava ---")

        self.is_logged = (
            False if soup.select_one(self.avatar_oboarding_sel) is None else True
        )
        return self.is_logged
