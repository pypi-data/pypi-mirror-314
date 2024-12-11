import asyncio
import json
from pathlib import Path
import random
import pytest

from raphson_music_client import RaphsonMusicClient
from raphson_music_client.track import AudioFormat, DownloadableTrack


@pytest.fixture
async def client():
    config_path = Path("test_config.json")
    assert config_path.exists()
    with config_path.open() as config_fp:
        config = json.load(config_fp)
    client = RaphsonMusicClient()
    await client.setup(base_url=config["base_url"], token=config["token"], user_agent="client test suite")
    yield client
    await client.close()


async def get_random_track(client: RaphsonMusicClient) -> DownloadableTrack:
    playlist = random.choice(await client.playlists())
    return await client.choose_track(playlist)


async def test_choose_track(client: RaphsonMusicClient):
    track = await get_random_track(client)
    track2 = await client.get_track(track.path)
    assert track == track2


async def test_download_news(client: RaphsonMusicClient):
    await client.get_news()


async def test_now_playing(client: RaphsonMusicClient):
    track = await get_random_track(client)
    await client.submit_now_playing(track.path, random.randint(0, track.duration), bool(random.randint(0, 1)))


async def test_list_tracks(client: RaphsonMusicClient):
    playlist = random.choice(await client.playlists())
    tracks = await client.list_tracks(playlist.name)
    track = random.choice(tracks)
    await client.get_track(track.path)  # verify the track exists


# this test is at the end because it takes a while
async def test_download_track(client: RaphsonMusicClient):
    playlist = random.choice(await client.playlists())
    track = await client.choose_track(playlist)
    await asyncio.gather(*[track.download(format) for format in AudioFormat])
