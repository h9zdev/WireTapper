import pytest
from app import app, classify_device, fetch_real_world_data

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_classify_device():
    assert classify_device("Tesla Model 3", "bluetooth") == "car"
    assert classify_device("Sony WH-1000XM4", "router") == "headphone"
    assert classify_device("Generic Router", "router") == "router"

def test_fetch_real_world_data():
    data = fetch_real_world_data(51.505, -0.09, 'wifi')
    assert isinstance(data, list)
    assert len(data) > 0
    # check keys
    first_item = data[0]
    assert "lat" in first_item
    assert "lon" in first_item

def test_home_route(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_nearby_route(client):
    rv = client.get('/nearby?lat=51.505&lon=-0.09&mode=wifi')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert "devices" in json_data

def test_chatbot_match(client):
    rv = client.post('/chatgpt', json={"message": "What is OSINT?"})
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert "OSINT" in json_data["reply"]

def test_chatbot_fallback(client):
    rv = client.post('/chatgpt', json={"message": "Explain how wifi waves propagate."})
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert "reply" in json_data
