from uuid import uuid4

from core.config import BASE_URL


def generate_short_url() -> str:
    return f"{BASE_URL}/{uuid4()}"[:16]
