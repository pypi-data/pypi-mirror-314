import datetime
import logging
from typing import NamedTuple, Optional

from playwright.sync_api import sync_playwright, TimeoutError

logger = logging.getLogger(__name__)


class Recording(NamedTuple):
    location: str
    delay: Optional[str] = None
    source: Optional[str] = None


def record(dirname: str, duration: int, height: int, url: str, width: int) -> Recording:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            record_video_dir=dirname,
            record_video_size={"width": width, "height": height},
            viewport={"width": width, "height": height},
        )
        page = context.new_page()
        page.set_viewport_size({"width": width, "height": height})
        page.goto(url, wait_until="domcontentloaded")
        now = datetime.datetime.now(datetime.UTC)

        try:
            video = page.locator("video")
            video.wait_for(timeout=2000)
            ready = datetime.datetime.now(datetime.UTC)
            for source in video.locator("source").all():
                if source.get_attribute("type") == "video/mp4":
                    src, _, _ = source.get_attribute("src").partition("?")

            # Record until the end of the video, at which point the `video` element will be set
            # as hidden.
            page.locator("video").first.wait_for(state="hidden")
            checkpoint = datetime.datetime.now(datetime.UTC)

        except TimeoutError:
            ready = checkpoint = datetime.datetime.now(datetime.UTC)
            src = None

        recorded = (checkpoint - ready).total_seconds()
        logger.debug(f"Recorded {recorded}s so far")
        remaining = duration - recorded
        if remaining > 0:
            logger.debug(f"{remaining}s left to record")
            expression = (
                "window.recording = 1; setTimeout(() => { window.recording = 0 }, "
                + str(remaining * 1000)
                + ");"
            )
            page.evaluate(expression)
            page.wait_for_function("() => window.recording == 0")

        context.close()

        location = page.video.path()
        browser.close()

    delay = f"{1000 * (ready - now).total_seconds()}ms"

    return Recording(delay=delay, location=location, source=src)


def screenshot(filename: str, height: int, url: str, width: int) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_viewport_size({"width": width, "height": height})
        page.goto(url, wait_until="networkidle")
        page.screenshot(path=filename)
        browser.close()
