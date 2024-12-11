import asyncio
from dataclasses import dataclass
from enum import Enum
import json

from aiohttp import ClientSession

from raphson_music_client.lyrics import LyricsLine, PlainLyrics, TimeSyncedLyrics
from raphson_music_client.util import urlencode


class AudioFormat(Enum):
    WEBM_OPUS_HIGH = "webm_opus_high"
    WEBM_OPUS_LOW = "webm_opus_low"
    MP4_AAC = "mp4_aac"
    MP3_WITH_METADATA = "mp3_with_metadata"


@dataclass
class DownloadedTrack:
    track: "Track | None"
    audio: bytes
    image: bytes
    lyrics_json: str

    @property
    def lyrics(self) -> TimeSyncedLyrics | PlainLyrics | None:
        lyrics_dict = json.loads(self.lyrics_json)
        if lyrics_dict["type"] == "none":
            return None
        elif lyrics_dict["type"] == "plain":
            return PlainLyrics(lyrics_dict["source"], lyrics_dict["text"])
        elif lyrics_dict["type"] == "synced":
            text = [LyricsLine(line["start_time"], line["text"]) for line in lyrics_dict["text"]]
            return TimeSyncedLyrics(lyrics_dict["source"], text)
        else:
            raise ValueError()

    @property
    def lyrics_text(self) -> str | None:
        lyrics = self.lyrics
        if not lyrics:
            return None
        if isinstance(lyrics, TimeSyncedLyrics):
            lyrics = lyrics.to_plain()
        return lyrics.text


@dataclass
class Track:
    path: str
    display: str
    mtime: int
    duration: int
    title: str | None
    album: str | None
    album_artist: str | None
    year: int | None
    artists: list[str]

    @property
    def playlist(self):
        return self.path[self.path.index("/") :]


@dataclass
class DownloadableTrack(Track):
    _session: ClientSession

    async def get_audio(self, audio_format: AudioFormat) -> bytes:
        async with self._session.get(
            "/track/" + urlencode(self.path) + "/audio?type=" + audio_format.value
        ) as response:
            return await response.content.read()

    async def get_cover_image(self) -> bytes:
        async with self._session.get("/track/" + urlencode(self.path) + "/cover?quality=high") as response:
            return await response.content.read()

    async def get_lyrics_json(self) -> str:
        async with self._session.get("/track/" + urlencode(self.path) + "/lyrics") as response:
            return await response.text()

    async def download(self, audio_format: AudioFormat = AudioFormat.WEBM_OPUS_HIGH) -> DownloadedTrack:
        audio, image, lyrics_json = await asyncio.gather(
            self.get_audio(audio_format),
            self.get_cover_image(),
            self.get_lyrics_json(),
        )
        return DownloadedTrack(self, audio, image, lyrics_json)

    async def download_mp3(self):
        return await self.get_audio(AudioFormat.MP3_WITH_METADATA)
