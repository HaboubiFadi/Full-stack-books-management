import time
import pytest
from src.books.schemas import Status
prefix="/api/v1/books"
@pytest.mark.asyncio
async def test_create_get_book(test_client , book_payload,book_uid):
    response = await test_client.post(f"{prefix}/", json=book_payload)
    response_json = response.json()
    assert response.status_code == 201
    uid=response_json['bookmodel']['uid']

    response = await test_client.get(f"{prefix}/{uid}")
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["Status"] == ["Success"]
    assert response_json["Book"]["title"] == "Think C++"
    assert response_json["Book"]["author"] == "Allen B. Downey"
    assert response_json["Book"]["publisher"] == "O'Reilly Media"
    assert response_json["Book"]["published_date"] == "2021-01-01"
    assert response_json["Book"]["page_count"] == 1234
    assert response_json["Book"]["language"] == "English"


    


