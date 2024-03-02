import os

import pytest
from sqlalchemy import text

from adapters.database import session_factory


@pytest.fixture
def api_url() -> str:
    return "{}:{}".format(
        "http://" + os.environ.get("API_SERVER", "localhost"),
        os.environ.get("API_PORT", 8080),
    )


@pytest.fixture(autouse=True, scope="function")
def clear_db() -> None:
    session = session_factory()
    session.execute(text("DELETE FROM url"))
    session.commit()
    session.close()
    return None
