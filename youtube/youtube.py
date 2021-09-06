from os import path
from yt_dlp import YoutubeDL
from config import DURATION_LIMIT
from helpers.errors import DurationLimitError

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ydl_opts = {
    "format": "bestaudio/best",
    "verbose": True,
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def download(song):
    duration = round(song["duration"] / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"Videos longer than {DURATION_LIMIT} minute(s) aren't allowed, the provided video is {duration} minute(s)"
        )
    ydl.download([song['webpage_url']])
    return path.join("downloads", f"{song['id']}.{song['ext']}")

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
