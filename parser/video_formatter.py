from datetime import datetime


def _sort_videos_desc(videos: list) -> list:
    def parse_date(v):
        try:
            return datetime.strptime(v["publish_date"], "%d/%m/%Y")
        except Exception:
            return datetime.min

    return sorted(videos, key=parse_date, reverse=True)


def build_video_text(products: list) -> str:
    lines = []

    for product in products:
        product_name = product["product"]
        videos = _sort_videos_desc(product.get("videos", []))

        for index, video in enumerate(videos, start=1):
            day = video.get("publish_date", "")
            url = video.get("url", "")

            lines.append(
                f"{product_name} {index} ({day}): {url}"
            )

        if videos:
            lines.append("")

    return "\n".join(lines).strip()