from dataclasses import dataclass
from aiohttp import ClientSession, ClientTimeout

from raphson_music_client.track import Track


@dataclass
class PlayerState:
    all_playlists: list[str]
    enabled_playlists: list[str]
    has_media: bool
    is_playing: bool
    position: int
    duration: int
    volume: float
    track: Track | None


class HeadlessPlayerClient:
    _session: ClientSession

    def __init__(self):
        self._session = None  # pyright: ignore[reportAttributeAccessIssue]

    async def setup(self, *, base_url: str) -> None:
        self._session = ClientSession(
            base_url=base_url,
            timeout=ClientTimeout(connect=5, total=60),
            raise_for_status=True,
        )

    async def state(self) -> PlayerState:
        response = await self._session.get("/state")
        json = await response.json()
        currently_playing = json["currently_playing"]
        if currently_playing:
            track = Track(
                currently_playing["path"],
                currently_playing["path"],  # TODO proper display string
                0,  # TODO mtime
                currently_playing["duration"],
                currently_playing["title"],
                currently_playing["album"],
                currently_playing["album_artist"],
                currently_playing["year"],
                currently_playing["artists"],
            )
        else:
            track = None

        return PlayerState(
            json["playlists"]["all"],
            json["playlists"]["enabled"],
            json["player"]["has_media"],
            json["player"]["is_playing"],
            json["player"]["position"],
            json["player"]["duration"],
            json["player"]["volume"] / 100,
            track,
        )

    async def list_tracks(self, playlist: str) -> list[Track]:
        async with self._session.get("/list_tracks", params={"playlist": playlist}) as response:
            response_json = await response.json()
        tracks: list[Track] = []
        for track_json in response_json:
            tracks.append(
                Track(
                    track_json["path"],
                    track_json["display"],
                    track_json["mtime"],
                    track_json["duration"],
                    track_json["title"],
                    track_json["album"],
                    track_json["album_artist"],
                    track_json["year"],
                    track_json["artists"],
                )
            )
        return tracks

    async def stop(self) -> None:
        async with self._session.post("/stop"):
            pass

    async def pause(self) -> None:
        async with self._session.post("/pause"):
            pass

    async def play(self) -> None:
        async with self._session.post("/play"):
            pass

    async def next(self) -> None:
        async with self._session.post("/next"):
            pass

    async def play_news(self) -> None:
        async with self._session.post("/play_news"):
            pass

    async def seek(self, position: int) -> None:
        async with self._session.post("/seek", data=str(position)):
            pass

    async def set_volume(self, volume: float) -> None:
        async with self._session.post("/volume", data=str(int(volume * 100))):
            pass

    async def set_enabled_playlists(self, playlists: list[str]) -> None:
        async with self._session.post("/playlists", json=playlists):
            pass

    async def enqueue(self, track: str | Track) -> None:
        if isinstance(track, Track):
            track = track.path
        async with self._session.post("/enqueue", data=track):
            pass

    async def play_track(self, track: str | Track) -> None:
        if isinstance(track, Track):
            track = track.path
        async with self._session.post("/play_track", data=track):
            pass
