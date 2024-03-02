from time import sleep

import requests as r

from core.config import BASE_URL

TEST_URL = "https://www.google.com/travel/flights/booking?tbo=1q=flightstcfs=UgJgAQguci="
URL_LENGTH = 16


def test_create_short_url(api_url: str) -> None:
    response = r.post(f"{api_url}", json={"url": TEST_URL})

    assert response.status_code == 201


def test_create_short_url_raises_409_when_url_already_exists(api_url: str) -> None:
    response = r.post(f"{api_url}", json={"url": TEST_URL})
    assert response.status_code == 201

    response = r.post(f"{api_url}", json={"url": TEST_URL})
    assert response.status_code == 409
    assert response.json()["detail"] == f"Url: {TEST_URL} already exists!"


def test_get_data_by_url(api_url: str) -> None:
    response = r.post(f"{api_url}", json={"url": TEST_URL})
    assert response.status_code == 201
    sleep(0.1)

    response = r.get(f"{api_url}?url={TEST_URL}")
    assert response.status_code == 200

    resp_json = response.json()
    assert resp_json["url"] == TEST_URL
    assert resp_json["short_url"].startswith(BASE_URL)
    assert len(resp_json["short_url"]) == URL_LENGTH


def test_get_data_by_url_raises_404_when_url_does_not_exist(api_url: str) -> None:
    url = "invalid_url"
    response = r.get(f"{api_url}?url={url}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Url: {url} does not exist!"


def test_get_data_by_short_url(api_url: str) -> None:
    response = r.post(f"{api_url}", json={"url": TEST_URL})
    assert response.status_code == 201
    sleep(0.1)

    response = r.get(f"{api_url}?url={TEST_URL}")
    assert response.status_code == 200
    full_url_resp_json = response.json()

    short_url = full_url_resp_json["short_url"]

    response = r.get(f"{api_url}/short_url?short_url={short_url}")
    assert response.status_code == 200
    assert response.json() == full_url_resp_json


def test_get_data_by_short_url_raises_404_when_short_url_does_not_exist(api_url: str) -> None:
    short_url = "invalid_short_url"
    response = r.get(f"{api_url}/short_url?short_url={short_url}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Short URL: {short_url} does not exist!"


def test_get_all_urls(api_url: str) -> None:
    response = r.post(f"{api_url}", json={"url": TEST_URL})
    assert response.status_code == 201
    sleep(0.1)

    response = r.get(f"{api_url}/all")
    assert response.status_code == 200
    assert len(response.json()) == 1

    assert response.json()[0]["url"] == TEST_URL
    assert response.json()[0]["short_url"].startswith(BASE_URL)
    assert len(response.json()[0]["short_url"]) == URL_LENGTH


def test_delete_url(api_url: str) -> None:
    response = r.post(f"{api_url}", json={"url": TEST_URL})
    assert response.status_code == 201

    response = r.get(f"{api_url}?url={TEST_URL}")
    assert response.status_code == 200
    url_id = response.json()["id"]

    response = r.delete(f"{api_url}/{url_id}")
    assert response.status_code == 204

    response = r.get(f"{api_url}?url={TEST_URL}")
    assert response.status_code == 404


def test_delete_url_raises_404_when_url_does_not_exist(api_url: str) -> None:
    url_id = 19999
    response = r.delete(f"{api_url}/{url_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Url with id: {url_id} does not exist!"
