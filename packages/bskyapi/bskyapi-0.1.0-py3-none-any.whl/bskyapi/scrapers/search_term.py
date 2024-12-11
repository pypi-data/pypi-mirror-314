import time
import typing as t
from bskyapi.clients import BskyApiClient
from atproto import models


class SearchTermScraper:
    def __init__(self, bsky_client: BskyApiClient):
        self.bsky_client = bsky_client
    
    def _fetch(self, search_term: str, cursor: t.Union[int, None] = None) -> models.AppBskyFeedSearchPosts.Response:
        params = {"q": search_term, 'limit': 100}
        if cursor:
            params['cursor'] = cursor
        return self.bsky_client.client.app.bsky.feed.search_posts(params=params)

    def fetch_all_posts(self, search_term: str, limit: int = 1000) -> t.List[models.AppBskyFeedSearchPosts.Response]:
        all_posts = []
        cursor = None
        while True:
            response = self._fetch(search_term, cursor)
            cursor = response.cursor
            posts = response.model_dump()['posts']
            all_posts.extend(posts)
            if not cursor:
                break
            if int(cursor) > limit:
                break
            time.sleep(2)
        return all_posts
