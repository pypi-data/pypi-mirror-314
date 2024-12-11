from dataclasses import dataclass


@dataclass
class LyricsLine:
    start_time: float
    text: str


@dataclass
class TimeSyncedLyrics:
    source: str
    text: list[LyricsLine]

    def to_plain(self) -> "PlainLyrics":
        text = "\n".join([line.text for line in self.text])
        return PlainLyrics(self.source, text)


@dataclass
class PlainLyrics:
    source: str
    text: str
