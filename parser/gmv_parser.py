import re


def parse_gmv(text: str):
    text = text.strip().replace(" ", "")

    if text == "1M₫+":
        return None, True

    text = text.replace("₫", "")

    if "Tỷ" in text:
        value = float(text.replace("Tỷ", "").replace(",", "."))
        return value * 1_000_000_000, False

    if text.endswith("T"):
        value = float(text.replace("T", "").replace(",", "."))
        return value * 1_000_000_000, False

    if "Tr" in text:
        value = float(text.replace("Tr", "").replace(",", "."))
        return value * 1_000_000, False

    return None, False


def parse_sales(text: str):
    text = text.strip().replace(" ", "")

    if text.endswith("Tr"):
        value = float(text.replace("Tr", "").replace(",", "."))
        return int(value * 1_000_000)

    if text.endswith("K"):
        value = float(text.replace("K", "").replace(",", "."))
        return int(value * 1000)

    digits = re.sub(r"[^\d]", "", text)

    return int(digits) if digits else 0