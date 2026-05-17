import re
from pathlib import Path


APP_PATH = Path("app/streamlit_app.py")
MIN_NORMAL_TEXT_RATIO = 4.5


def relative_luminance(hex_color: str) -> float:
    value = hex_color.strip().lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", value):
        raise ValueError(f"Invalid color: {hex_color}")

    channels = [int(value[index : index + 2], 16) / 255 for index in (0, 2, 4)]
    linear_channels = [
        channel / 12.92
        if channel <= 0.03928
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    red, green, blue = linear_channels
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(foreground: str, background: str) -> float:
    foreground_luminance = relative_luminance(foreground)
    background_luminance = relative_luminance(background)
    lighter = max(foreground_luminance, background_luminance)
    darker = min(foreground_luminance, background_luminance)
    return (lighter + 0.05) / (darker + 0.05)


def css_variables(source: str) -> dict[str, str]:
    return dict(re.findall(r"--([a-z0-9-]+):\s*(#[0-9a-fA-F]{6});", source))


def assert_min_contrast(name: str, foreground: str, background: str) -> None:
    ratio = contrast_ratio(foreground, background)
    if ratio < MIN_NORMAL_TEXT_RATIO:
        raise SystemExit(
            f"ux-a11y: {name} contrast {ratio:.2f}:1 is below "
            f"{MIN_NORMAL_TEXT_RATIO}:1 ({foreground} on {background})"
        )


def main() -> None:
    source = APP_PATH.read_text(encoding="utf-8")
    variables = css_variables(source)

    required_tokens = {
        "empathy-ink",
        "empathy-muted",
        "empathy-teal-dark",
        "empathy-coral-dark",
    }
    missing_tokens = required_tokens - set(variables)
    if missing_tokens:
        raise SystemExit(f"ux-a11y: missing CSS tokens: {sorted(missing_tokens)}")

    assert_min_contrast("body text", variables["empathy-ink"], "#ffffff")
    assert_min_contrast("secondary text", "#595959", "#ffffff")
    assert_min_contrast("accent label", variables["empathy-teal-dark"], "#ffffff")
    assert_min_contrast("primary button teal side", "#ffffff", variables["empathy-teal-dark"])
    assert_min_contrast("primary button coral side", "#ffffff", variables["empathy-coral-dark"])

    if "@media (max-width: 760px)" not in source:
        raise SystemExit("ux-a11y: missing small-screen media query")

    for focus_selector in (".stAudioInput:focus-within", ".stButton > button:focus-visible"):
        if focus_selector not in source:
            raise SystemExit(f"ux-a11y: missing focus selector {focus_selector}")

    if 'st.button(t("analyze"), type="primary", use_container_width=True)' not in source:
        raise SystemExit("ux-a11y: primary analyze action is not full width")

    if "st.audio_input(" not in source:
        raise SystemExit("ux-a11y: optional audio input is missing from the demo UI")
    if "render_session_timeout_guard(settings)" not in source:
        raise SystemExit("ux-a11y: session timeout guard is not rendered")
    if "mousemove" not in source or "keydown" not in source or "touchstart" not in source:
        raise SystemExit("ux-a11y: timeout guard must watch human interaction events")
    if "_stcore/health" in source or "_stcore/stream" in source:
        raise SystemExit("ux-a11y: timeout guard should not depend on Streamlit health traffic")
    if "Session will expire soon due to inactivity" not in source:
        raise SystemExit("ux-a11y: timeout warning copy is missing")

    print("ux-a11y: ok")


if __name__ == "__main__":
    main()
