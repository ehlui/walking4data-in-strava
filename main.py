from core.strava import *


if __name__ == "__main__":
    """Example of current usage"""
    
    print('Running script directly ...')

    print('1. Reading athletes with ids - 80149432, 7396778 ')
    strava_users = strava_users_api()

    athletes = strava_users.get_users(["80149432", "7396778"])
    print(f'\t> FOUND: \n{athletes}\n')

    print('***'*10)
    
    print('2. Searching athletes by - <jaume gomez> ')
    athletes_id = strava_users.search_users("jaume gomez")
    print(f'\t> FOUND: \n{athletes_id}\n')
