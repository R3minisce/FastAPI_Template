import pytest

from httpx import AsyncClient

from main import app


name, description = ["teseeet123", "super desc"]
data = {"name": name, "description": description}
data_put = {"name": name + "_put", "description": description}

BASE_URL = "https://localhost:8000/parent"

"""
# Feel free to adapt tests depending on your needs
"""


@pytest.mark.asyncio
async def test_parent_get_empty():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("")
        assert response.status_code == 200
        assert response.json() == dict(items=[], total=0, page=1, size=50)


@pytest.mark.asyncio
async def test_parent_post():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        # Adding an id to the URL
        response = await ac.post("/2", json=data_put)
        assert response.status_code == 405

        # Without Json
        response = await ac.post("")
        assert response.status_code == 422

        # Malformed Json
        response = await ac.post("", json="aaa")
        assert response.status_code == 422

        # Missing parts Json
        response = await ac.post("", json={"description": description})
        assert response.status_code == 422

        # Not valid Json
        response = await ac.post("", json={"description": description, "name": "cour"})
        assert response.status_code == 422

        # Valid Json
        response = await ac.post("", json=data)
        assert response.status_code == 201
        assert response.json() == dict(data, id=1)


@pytest.mark.asyncio
async def test_parent_get_all():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("")
        assert response.status_code == 200
        assert response.json() == dict(items=[dict(data, id=1)], total=1, page=1, size=50)


@pytest.mark.asyncio
async def test_parent_get_one():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        # Id not in DB
        response = await ac.get("/2")
        assert response.status_code == 404

        # Without Id
        response = await ac.get("/")
        assert response.status_code == 200

        # Id as str
        response = await ac.get("/aze")
        assert response.status_code == 422

        # Id as double
        response = await ac.get("/5.2")
        assert response.status_code == 422

        # Valid
        response = await ac.get("/1")
        assert response.status_code == 200
        assert response.json() == dict(data, id=1, children=[])


@pytest.mark.asyncio
async def test_parent_put():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        # Id not in DB
        response = await ac.put("/2", json=data_put)
        assert response.status_code == 404

        # Without Id
        response = await ac.put("/", json=data_put)
        assert response.status_code == 405

        # Id as str
        response = await ac.put("/aze", json=data_put)
        assert response.status_code == 422

        # Id as double
        response = await ac.put("/5.2", json=data_put)
        assert response.status_code == 422

        # Without Json
        response = await ac.put("/1")
        assert response.status_code == 422

        # Valid id but missing parts Json
        response = await ac.put("/1", json={"description": description})
        assert response.status_code == 422

        # Valid Id but not valid Json
        response = await ac.put("/1", json={"description": description, "name": "cour"})
        assert response.status_code == 422

        # Valid
        response = await ac.put("/1", json=data_put)
        assert response.status_code == 200
        assert response.json() == dict(data_put, id=1)
        # And verification
        response = await ac.get("/1")
        assert response.status_code == 200
        assert response.json() == dict(data_put, id=1, children=[])


@pytest.mark.asyncio
async def test_parent_delete():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        # Id not in DB
        response = await ac.delete("/2")
        assert response.status_code == 404

        # Without Id
        response = await ac.delete("/")
        assert response.status_code == 405

        # Id as str
        response = await ac.delete("/aze")
        assert response.status_code == 422

        # Id as double
        response = await ac.delete("/4.45")
        assert response.status_code == 422

        # Valid
        response = await ac.delete("/1")
        assert response.status_code == 200
        # And verification
        response = await ac.get("/1")
        assert response.status_code == 404
