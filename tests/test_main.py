from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

SAMPLE = {
    "title": "Test Product",
    "description": "Created by the test suite",
    "at_sale": False,
    "inventory": 1,
}


def free_id():
    """Create a product then delete it, returning an id guaranteed not to exist."""
    created = client.post("/product", json=SAMPLE)
    assert created.status_code == 200
    product_id = created.json()["id"]
    assert client.delete(f"/delete/{product_id}").status_code == 204
    return product_id


def test_update_missing_product_returns_404():
    missing_id = free_id()

    response = client.put(f"/update/{missing_id}", json=SAMPLE)

    assert response.status_code == 404
    assert str(missing_id) in response.json()["detail"]


def test_delete_missing_product_returns_404():
    missing_id = free_id()

    response = client.delete(f"/delete/{missing_id}")

    assert response.status_code == 404
    assert str(missing_id) in response.json()["detail"]
