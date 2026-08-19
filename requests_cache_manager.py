import requests_cache

session = requests_cache.CachedSession(
    urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE, #do not cache stuff from this URL
        "*": 3600, #all other requests will be cached for an hour only
        })
