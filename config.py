from os import getenv


config = {
    'debug_guilds': [int(i) for i in getenv('DEBUG_GUILDS').split(' ')] if getenv('DEBUG_GUILDS') else [],
    'owner_id': int(getenv('OWNER_ID')),
}