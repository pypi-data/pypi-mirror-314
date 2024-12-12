__all__ = ["Options", "run"]

import logging
import shutil
import tempfile
from pathlib import Path
from typing import NamedTuple, Optional

from .aws import upload
from .browser import record, screenshot
from .media import convert, merge
from .web import download

logger = logging.getLogger(__name__)


class Options(NamedTuple):
    url: str
    width: int
    height: int
    format: str
    duration: Optional[int] = 6
    path: Optional[str] = "/tmp"
    output: Optional[str] = "."
    filename: Optional[str] = None


def filename(output, filename):
    if output.startswith("s3://"):
        return "s3://" + str(Path(output[5:]) / filename)

    return str(Path(output) / filename)


def add_audio(filename: str, path: Path) -> None:
    """Add audio stream.

    The source of the audio is extracted from a "source.mp4" video file found in the `path`.
    The video file is first renamed because FFmpeg cannot edit existing files in-place.
    """
    source = str(path / "source.mp4")
    audio = str(path / "audio.mp3")
    convert(infile=source, outfile=audio)

    video = str(path / f"_{filename}")
    shutil.move(path / filename, video)
    merge(infiles=[video, audio], outfile=str(path / filename))


def capture(filename: str, options: Options, path: Path) -> None:
    recording = record(
        dirname=str(path),
        duration=options.duration,
        height=options.height,
        url=options.url,
        width=options.width,
    )
    convert(
        infile=recording.location,
        outfile=str(path / filename),
        delay=recording.delay,
        # use highest quality, and place MOOV atom at the beginning
        opts=["-crf", "1", "-movflags", "faststart"],
    )
    if recording.source:
        logger.info(f"Adding audio from {recording.source}")
        download(url=recording.source, filename=str(path / "source.mp4"))
        add_audio(filename=filename, path=path)

    file = str(path / filename)
    copy = str(path / f"_{filename}")
    shutil.move(file, copy)
    convert(
        infile=copy,
        outfile=file,
        duration=options.duration,
        opts=["-c", "copy"],
    )


def screengrab(filename: str, options: Options, path: Path) -> None:
    screenshot(
        filename=str(path / filename),
        height=options.height,
        url=options.url,
        width=options.width,
    )


def run(options: Options) -> None:
    with tempfile.TemporaryDirectory(dir=options.path) as dirname:
        path = Path(dirname)
        logger.debug(f"Working directory: '{path}'")
        if options.format == "video":
            asset = options.filename or "video.mp4"
            output = filename(options.output, asset)
            logger.info(
                f"Capturing '{options.url}' [{options.width}x{options.height}]"
                f" for {options.duration}s to '{output}'",
            )
            capture(filename=asset, options=options, path=path)
        else:
            asset = options.filename or "screenshot.png"
            output = filename(options.output, asset)
            logger.info(
                f"Taking screenshot of '{options.url}' [{options.width}x{options.height}]"
                f" to '{output}'"
            )
            screengrab(filename=asset, options=options, path=path)

        if output.startswith("s3://"):
            upload(str(path / asset), output)
        else:
            shutil.copy(path / asset, output)
