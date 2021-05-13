# anidb crawler

## Disclaimer

Site owners tend to hate web crawlers and anidb is no exception. Always prefer
official APIs and language-specific bindings to them, if possible

## Description

Thou shall be bs4-powered library to fetch various data from anidb site, without
relying on any API. Im making it solely for my discord server's bot to use and
right now its extremely WIP

## Requirements
- python 3.8+
- beautifulsoup4
- requests

## Usage Example

```python3
import anidb_crawler as ac

fetcher = ac.AnidbFetcher(user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0")
client = ac.AnidbClient(fetcher_instance = fetcher)

client.get_anime(99)
```

## Limitations
- **There wont be async support**. I initially planned to implement it, but since
flooding anidb with requests will bring your IP to their blacklist - I stepped
back on that decision
- Because web crawlers are banned by anidb, **in order to use this library, you
must supply it with real browser's user agent**
