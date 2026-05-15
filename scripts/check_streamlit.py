import sys
from urllib.error import URLError
from urllib.request import urlopen


DEFAULT_URL = "http://localhost:8501"


def main(url=DEFAULT_URL):
    try:
        with urlopen(url, timeout=10) as response:
            status = response.status
    except URLError as error:
        raise SystemExit(f"streamlit-ui: unavailable ({error})") from error

    if status != 200:
        raise SystemExit(f"streamlit-ui: unexpected status {status}")

    print(f"streamlit-ui: ok ({url})")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL)
