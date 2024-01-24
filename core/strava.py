from core.stravasession import StravaSession
from core.stravausers import StravaUsers


def strava_users_api() -> StravaUsers:
    return StravaUsers(strava_session=StravaSession())
