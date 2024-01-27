from core.strava import *


if __name__ == "__main__":
    from pprint import pprint

    def print_dict(data:list):
        pprint(data)


    """Example of current usage"""
    
    print('Running script directly ...')

    ids=["80149432", "7396778"]
    print(f'1. Reading athletes with ids - {ids} ')
    strava_users = strava_users_api()

    athletes = strava_users.get_users(ids)
    print(f'\t> FOUND: \n')
    print_dict(athletes)

    print('\n********************************\n')
    
    searchname='jaume gomez'
    print(f'2. Searching athletes by - <{searchname}> ')
    athletes_ids = strava_users.search_users(searchname)
    print(f'\t> FOUND: \n')
    print_dict(athletes_ids)

    print('\n********************************\n')
