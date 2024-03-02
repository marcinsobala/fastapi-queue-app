from core.config import BASE_URL
from core.url_shortener import generate_short_url


def test_shorten_url() -> None:
    short_url = generate_short_url()
    assert len(short_url) == 16
    assert short_url.startswith(BASE_URL)
