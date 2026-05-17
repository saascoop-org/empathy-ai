from html.parser import HTMLParser
from pathlib import Path


LANDING_PATH = Path("landing/index.html")
REQUIRED_VIDEO_IDS = {
    "sA26L7lsu2M",
    "urQLq7XPmMo",
    "QglZuuNpIpM",
    "OXi9H7ybFT4",
    "msrbxW9grXk",
    "ZjnyZeH075k",
}
REQUIRED_LANGUAGES = {"en", "pt", "es"}


class LandingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.language_layers = set()
        self.language_buttons = set()
        self.iframes = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "data-language" in attributes:
            self.language_layers.add(attributes["data-language"])
        if "data-language-button" in attributes:
            self.language_buttons.add(attributes["data-language-button"])
        if tag == "iframe":
            self.iframes.append(attributes.get("src", ""))
        if tag == "a":
            self.links.append(attributes.get("href", ""))


def main() -> None:
    source = LANDING_PATH.read_text(encoding="utf-8")
    parser = LandingParser()
    parser.feed(source)

    if parser.language_layers != REQUIRED_LANGUAGES:
        raise SystemExit(f"landing: language layers mismatch: {parser.language_layers}")
    if parser.language_buttons != REQUIRED_LANGUAGES:
        raise SystemExit(f"landing: language buttons mismatch: {parser.language_buttons}")

    missing_videos = [
        video_id
        for video_id in REQUIRED_VIDEO_IDS
        if f"https://www.youtube.com/embed/{video_id}" not in parser.iframes
    ]
    if missing_videos:
        raise SystemExit(f"landing: missing video embeds: {missing_videos}")

    if "../images/EmpathyAI_logo.png" not in source:
        raise SystemExit("landing: missing EmpathyAI logo asset reference")
    if "Access controlled demo" not in source:
        raise SystemExit("landing: missing English CTA")
    if "Acessar demo controlada" not in source:
        raise SystemExit("landing: missing Portuguese CTA")
    if "Acceder a la demo controlada" not in source:
        raise SystemExit("landing: missing Spanish CTA")
    if "@media (max-width: 860px)" not in source:
        raise SystemExit("landing: missing responsive breakpoint")

    print("landing: ok")


if __name__ == "__main__":
    main()
