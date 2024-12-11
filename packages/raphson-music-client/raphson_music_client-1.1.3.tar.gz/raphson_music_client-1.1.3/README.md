# music-client-python

Python client library for interacting with the Raphson music server. For use in other applications.

## Installation

This library is available [on PyPi](https://pypi.org/project/raphson-music-client/).

Install it using pip:
```
pip install raphson-music-client
```

## Usage

```py
import asyncio
from raphson_music_client import RaphsonMusicClient

async def main():
    client = RaphsonMusicClient()
    await client.setup(base_url=..., user_agent=..., token=...)

if __name__ == '__main__'
    asyncio.run(main())
```
