import time
import typing as t
from bskyapi.clients import BskyApiClient
from atproto import models


class ProfileScraper:
    def __init__(self, bsky_client: BskyApiClient):
        self.bsky_client = bsky_client
    

    def _fetch_follows(self, actor: str, cursor: t.Union[str, None] = None) -> models.AppBskyGraphGetFollows.Response:
        params = models.AppBskyGraphGetFollows.Params(actor=actor, limit=100)
        if cursor:
            params.cursor = cursor
        return self.bsky_client.client.app.bsky.graph.get_follows(params)

    def _fetch_followers(self, actor: str, cursor: t.Union[str, None] = None) -> models.AppBskyGraphGetFollowers.Response:
        params = models.AppBskyGraphGetFollowers.Params(actor=actor, limit=100)
        if cursor:
            params.cursor = cursor
        return self.bsky_client.client.app.bsky.graph.get_followers(params)
    
    def fetch_all_profiles(self, actors: list) -> models.AppBskyActorGetProfiles.Response:
        return self.bsky_client.client.get_profiles(actors)
    
    def fetch_all_follows(self, actor: str, limit: int = 1000) -> t.List[models.AppBskyGraphGetFollows.Response]:
        limit_check = 0
        all_follows = []
        cursor = None
        while True:
            limit_check += 100
            response = self._fetch_follows(actor, cursor)
            cursor = response.cursor
            follows = response.model_dump()['follows']
            all_follows.extend(follows)
            if not cursor:
                break
            if limit_check > limit:
                break
            time.sleep(2)
        return all_follows
    
    def fetch_all_followers(self, actor: str, limit: int = 1000) -> t.List[models.AppBskyGraphGetFollowers.Response]:
        limit_check = 0
        all_followers = []
        cursor = None
        while True:
            limit_check += 100
            response = self._fetch_followers(actor, cursor)
            cursor = response.cursor
            followers = response.model_dump()['followers']
            all_followers.extend(followers)
            if not cursor:
                break
            if limit_check > limit:
                break
            time.sleep(2)
        return all_followers
