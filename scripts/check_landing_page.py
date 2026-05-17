from html.parser import HTMLParser
from pathlib import Path


LANDING_PATH = Path("landing/index.html")
SESSION_EXPIRED_PATH = Path("landing/session-expired.html")
ROOT_SESSION_EXPIRED_PATH = Path("session-expired.html")
LAUNCHER_ENDPOINT = (
    "https://empathyai-demo-launcher-213729457903.us-central1.run.app/start-demo"
)
REQUIRED_VIDEO_IDS = {
    "sA26L7lsu2M",
    "urQLq7XPmMo",
    "QglZuuNpIpM",
    "OXi9H7ybFT4",
    "msrbxW9grXk",
    "ZjnyZeH075k",
}
REQUIRED_LANGUAGES = {"en", "pt", "es"}
REQUIRED_SCREENSHOTS = {
    "screenshot-EN-1.png",
    "screenshot-EN-2.png",
    "screenshot-EN-3.png",
    "screenshot-EN-4.png",
    "screenshot-PT-BR-1.png",
    "screenshot-PT-BR-2.png",
    "screenshot-PT-BR-3.png",
    "screenshot-PT-BR-4.png",
    "screenshot-ES-1.png",
    "screenshot-ES-2.png",
    "screenshot-ES-3.png",
    "screenshot-ES-4.png",
}


class LandingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.language_layers = set()
        self.language_buttons = set()
        self.iframes = []
        self.images = []
        self.links = []
        self.launch_buttons = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "data-language" in attributes:
            self.language_layers.add(attributes["data-language"])
        if "data-language-button" in attributes:
            self.language_buttons.add(attributes["data-language-button"])
        if tag == "iframe":
            self.iframes.append(attributes.get("src", ""))
        if tag == "img":
            self.images.append(attributes.get("src", ""))
        if tag == "a":
            self.links.append(attributes.get("href", ""))
        if "data-launch-demo" in attributes:
            self.launch_buttons += 1


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

    missing_screenshots = [
        screenshot
        for screenshot in REQUIRED_SCREENSHOTS
        if f"../images/{screenshot}" not in parser.images
    ]
    if missing_screenshots:
        raise SystemExit(f"landing: missing screenshot references: {missing_screenshots}")

    if "Launch Controlled Demo" not in source:
        raise SystemExit("landing: missing English CTA")
    if "Iniciar demo controlada" not in source:
        raise SystemExit("landing: missing Portuguese CTA")
    if "Iniciar demo controlada" not in source:
        raise SystemExit("landing: missing Spanish CTA")
    if parser.launch_buttons != 3:
        raise SystemExit(f"landing: expected 3 launch buttons, found {parser.launch_buttons}")
    if LAUNCHER_ENDPOINT not in source:
        raise SystemExit("landing: missing Cloud Run launcher endpoint")
    for launch_text in (
        "Initializing local AI runtime...",
        "Loading empathy mediation agents...",
        "Preparing secure controlled session...",
        "Launching experience...",
        "launcher CORS policy is updated",
        "Access-Control-Allow-Origin for https://hackathonbrteam.github.io",
        "automatic session shutdown to minimize infrastructure and environmental costs",
    ):
        if launch_text not in source:
            raise SystemExit(f"landing: missing launch lifecycle text: {launch_text}")
    for launch_token in (
        "fetch(launcherEndpoint",
        "readTokenizedDemoUrl(demoUrl, payload)",
        "payload.auth_url || payload.authUrl || payload.authURL",
        "payload.demo_token || payload.demoToken || payload.token",
        'url.searchParams.set("demo_token", demoToken)',
        "readDemoUrl(payload)",
        "window.location.assign(demoUrl)",
        "button.disabled = isDisabled",
    ):
        if launch_token not in source:
            raise SystemExit(f"landing: missing launch behavior token: {launch_token}")
    for unsafe_token in ("url.username", "url.password", "payload.password", "credentials.password"):
        if unsafe_token in source:
            raise SystemExit(f"landing: must not expose Basic Auth credential handling: {unsafe_token}")
    if "@media (max-width: 860px)" not in source:
        raise SystemExit("landing: missing responsive breakpoint")
    if "function detectPreferredLanguage()" not in source:
        raise SystemExit("landing: missing browser language detection")
    if 'const fallbackLanguage = "en";' not in source:
        raise SystemExit("landing: missing explicit English fallback")
    for language_prefix in ('startsWith("pt")', 'startsWith("es")', 'startsWith("en")'):
        if language_prefix not in source:
            raise SystemExit(f"landing: missing language prefix rule {language_prefix}")

    expired_source = SESSION_EXPIRED_PATH.read_text(encoding="utf-8")
    if "Session expired" not in expired_source:
        raise SystemExit("landing: missing session expired page title")
    if "infrastructure and environmental costs" not in expired_source:
        raise SystemExit("landing: missing sustainability message")
    if "detectPreferredLanguage" not in expired_source:
        raise SystemExit("landing: session expired page missing language detection")

    root_expired_source = ROOT_SESSION_EXPIRED_PATH.read_text(encoding="utf-8")
    if "landing/session-expired.html" not in root_expired_source:
        raise SystemExit("landing: root session-expired redirect is missing")

    print("landing: ok")


if __name__ == "__main__":
    main()
