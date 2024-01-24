from core.stravasession import StravaSession
from core.domain.athletes import Athlete
from core.requestheaders import headers as strava_headers
from core.utils.helpers import fetch_html_parsed, get_base_url
from bs4 import BeautifulSoup


class StravaUsers:
    sleep_range = (2, 8)
    next_page_cache: str = ""
    strava_session: StravaSession
    headers: dict
    athlete_profile_selectors = {
        "name": "h1.athlete-name",
        "title": "div.athlete-title",
        "location": "div.location",
        "avatar_url": "div.profile-heading  img.avatar-img",
    }
    selectors = {
        "athletes": "div.athlete-details div.follow-action",
        "athlete_id_attr": "data-athlete-id",
        "next_page": "li.next_page a[rel='next']",
        "not_found_search": "p.text-callout",
    }

    def __init__(self, strava_session: StravaSession) -> None:
        if not strava_session.is_logged:
            strava_session.start()

        self.base_url = get_base_url()
        self.athlete_profle_url = f"{ self.base_url}/athletes"
        self.strava_session = strava_session
        self.headers = strava_headers["on_login"]

    def get_users(self, users_id: list[str]) -> list[Athlete]:
        """
        Extract athletes/users from strava by a list of ids
        :: Selecting data:
            = Name, title, country & profile image
        """
        url_template = f"{self.athlete_profle_url}/#"
        athletes = []
        for user_id in users_id:
            if not self.is_valid_id(user_id):
                print(f"ID <{user_id}> is not valid my 朋友!")
                continue

            url = url_template.replace("#", user_id)
            soup = fetch_html_parsed(
                url=url,
                session=self.strava_session.session,
                headers=self.headers,
                sleep_range=self.sleep_range,
            )

            if soup is None:
                continue

            collector = self.extract_athlete_content_from_html(soup=soup)
            print(collector)
            athletes.append(Athlete(**collector))

        return athletes

    def search_users(
        self, searching_name: str, all_pages: bool = True
    ) -> list[Athlete]:
        """
        Extract athletes/users searched by name
        :: Selecting data:
            = searching_name & users_id
        """
        if searching_name is None:
            return []

        search_result = {"search": searching_name}

        # spaces with +
        searching_name = searching_name.strip().replace(" ", "+")
        search_url = f"{self.athlete_profle_url}/search?utf8=✓&text={searching_name}"

        soup = fetch_html_parsed(
            url=search_url, session=self.strava_session.session, headers=self.headers
        )

        # 1. check if has results (any athlete)
        not_found_txt_css = self.selectors["not_found_search"]
        selector_nf = soup.select_one(not_found_txt_css)

        if selector_nf is not None:
            print(f"--- No athletes found by <{searching_name}> ---")
            return []

        # 2. check if has multiple pages
        athletes_selectors = soup.select(self.selectors["athletes"])
        search_result["athletes"] = []

        athletes_amount = len(athletes_selectors)
        idx = 0
        page_count = 1

        while idx < athletes_amount:
            athlete_sel = athletes_selectors[idx]

            if athlete_sel is None:
                continue

            athlete_id = athlete_sel.get(self.selectors["athlete_id_attr"], "-1")
            search_result["athletes"].append(athlete_id)

            # Go to next page before finishing the extraction
            if all_pages and idx == athletes_amount - 1:
                """Going next page to keep extracting athelets"""
                next_page_soup = self.extract_next_page(soup=soup)

                if next_page_soup is None:
                    break

                athletes_selectors = next_page_soup.select(self.selectors["athletes"])
                athletes_amount = len(athletes_selectors)
                page_count += 1

                # Restart loop in case we've got another page

                idx = 0
                continue

            idx += 1

        # print(
        #    f'Pages scraped <{page_count}> :: athletes found <{len(search_result.get("athletes"))}>'
        # )

        return search_result

    # return json.dumps(athlete.dict())

    def extract_next_page(self, soup: BeautifulSoup) -> BeautifulSoup:
        next_page_css = self.selectors["next_page"]
        next_page_selector = soup.select_one(next_page_css)

        if not next_page_selector:
            return None

        next_page_href_url = next_page_selector.get("href")
        url = f"{self.base_url}{next_page_href_url}"

        if url == self.next_page_cache:
            return None

        self.next_page_cache = url

        return fetch_html_parsed(
            url=url,
            session=self.strava_session.session,
            headers=self.headers,
            sleep_range=self.sleep_range,
        )

    def extract_athlete_content_from_html(self, soup: BeautifulSoup) -> dict[str]:
        collector = {}
        for k, v in self.athlete_profile_selectors.items():
            tag_result = soup.select_one(v)
            collector[k] = ""

            if tag_result is None:
                continue

            collector[k] = tag_result.text.replace("\n", "")

            if "avatar_url" in k:
                collector[k] = tag_result.get("src", "not-found")

        return collector

    def is_valid_id(self, id: str):
        """
        This logic should be in a dataclass or the domain instead of here,
        but for the sake for my precious time i put it here.
        """
        return True if id is not None and id.isnumeric() and int(id) > 0 else False
