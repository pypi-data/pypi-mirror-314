import asyncio
import uuid
from typing import Any

from aiohttp import ClientTimeout, StreamReader
from aiohttp.client import ClientSession

from raphson_music_client.playlist import Playlist
from raphson_music_client.track import DownloadableTrack, DownloadedTrack
from raphson_music_client.util import urlencode


class RaphsonMusicClient:
    player_id: str
    session: ClientSession
    cached_rapson_logo: bytes | None = None

    def __init__(self):
        self.player_id = str(uuid.uuid4())
        self.session = None  # pyright: ignore[reportAttributeAccessIssue]

    async def setup(self, *, base_url: str, user_agent: str, token: str) -> None:
        self.session = ClientSession(
            base_url=base_url,
            headers={"User-Agent": user_agent, "Authorization": "Bearer " + token},
            timeout=ClientTimeout(connect=5, total=60),
            raise_for_status=True,
        )

    async def close(self) -> None:
        if self.session:
            await self.session.close()

    def _track_from_json(self, json: dict[str, Any]) -> DownloadableTrack:
        assert self.session
        return DownloadableTrack(
            json["path"],
            json["display"],
            json["mtime"],
            json["duration"],
            json["title"],
            json["album"],
            json["album_artist"],
            json["year"],
            json["artists"],
            self.session,
        )

    async def choose_track(self, playlist: Playlist | str) -> DownloadableTrack:
        if isinstance(playlist, Playlist):
            playlist = playlist.name
        async with self.session.post("/playlist/" + urlencode(playlist) + "/choose_track", json={}) as response:
            json = await response.json()
        return self._track_from_json(json)

    async def get_track(self, path: str) -> DownloadableTrack:
        async with self.session.get("/track/" + urlencode(path) + "/info") as response:
            json = await response.json()
        return self._track_from_json(json)

    async def submit_now_playing(self, track_path: str, position: int, paused: bool) -> None:
        async with self.session.post(
            "/activity/now_playing",
            json={
                "player_id": self.player_id,
                "track": track_path,
                "paused": paused,
                "position": position,
            },
        ):
            pass

    async def submit_played(self, track_path: str, timestamp: int) -> None:
        async with self.session.post("/activity/played", json={"track": track_path, "timestamp": timestamp}):
            pass

    async def _get_news_audio(self) -> bytes:
        async with self.session.get("/news/audio") as response:
            return await response.content.read()

    async def get_news(self) -> DownloadedTrack:
        audio, image = await asyncio.gather(self._get_news_audio(), self.get_raphson_logo())
        return DownloadedTrack(None, audio, image, '{"type":"none"}')

    async def get_raphson_logo(self) -> bytes:
        if not self.cached_rapson_logo:
            async with self.session.get("/static/img/raphson.png") as response:
                self.cached_rapson_logo = await response.content.read()
        return self.cached_rapson_logo

    async def list_tracks_response(self, playlist: str) -> StreamReader:
        response = await self.session.get("/tracks/filter", params={"playlist": playlist})
        return response.content

    async def list_tracks(self, playlist: str) -> list[DownloadableTrack]:
        async with self.session.get("/tracks/filter", params={"playlist": playlist}) as response:
            response_json = await response.json()
        return [self._track_from_json(track_json) for track_json in response_json["tracks"]]

    async def playlists(self) -> list[Playlist]:
        async with self.session.get("/playlist/list") as response:
            return [Playlist(playlist["name"], playlist["favorite"]) for playlist in await response.json()]
