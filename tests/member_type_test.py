from fastapi.testclient import TestClient
from routes.member_type_router import router
from main import app

client = TestClient(app)


def test_get_member_type():
    response = client.get(f"{router.prefix}/get_member_type", params={"type_id": 1})

    assert response.status_code == 200
    assert response.json() == {
        "status": True,
        "message": "get data completed!",
        "data": {
            "member_type_name": "visitor",
            "id": 1
        }
    }

