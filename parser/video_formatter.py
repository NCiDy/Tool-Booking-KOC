from datetime import datetime
from config import FILTER_BY_DATE, START_DATE, END_DATE


def _parse_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except Exception:
        return None


def _sort_videos_desc(videos: list) -> list:
    return sorted(
        videos,
        key=lambda v: _parse_date(v.get("publish_date", "")) or datetime.min,
        reverse=True,
    )


def _filter_videos(videos: list) -> list:
    if not FILTER_BY_DATE:
        return videos

    start = _parse_date(START_DATE)
    end = _parse_date(END_DATE)

    if start is None or end is None:
        return videos

    result = []

    for video in videos:
        day = _parse_date(video.get("publish_date", ""))

        if day is None:
            continue

        if start <= day <= end:
            result.append(video)

    return result


def build_video_text(products: list) -> str:
    lines = []

    for product in products:
        product_name = product["product"]

        videos = _sort_videos_desc(product.get("videos", []))
        videos = _filter_videos(videos)

        for index, video in enumerate(videos, start=1):
            day = video.get("publish_date", "")
            url = video.get("url", "")

            lines.append(
                f"{product_name} {index}: {url}"
                #f"{product_name} {index} ({day}): {url}"
            )

        if videos:
            lines.append("")

    return "\n".join(lines).strip()