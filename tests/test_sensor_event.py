import pytest
from app import create_app
from app.utils.extension import socketio
import app.event.sensor_event  # penting untuk register event handler

@pytest.fixture
def client():
    """Buat Flask app dan test client SocketIO"""
    app = create_app()
    test_client = socketio.test_client(
        app,
        auth={"device_id": "dev123", "key": "dummykey1", "salt": "dummysalt1"}
    )
    yield test_client
    test_client.disconnect()

def test_successful_connection(client):
    """Cek koneksi valid"""
    assert client.is_connected()
    received = client.get_received()
    assert any(
        pkt["name"] == "message" and "authenticated" in pkt["args"]["msg"]
        for pkt in received
    )


def test_failed_connection():
    """Cek koneksi invalid"""
    app = create_app()
    bad_client = socketio.test_client(
        app,
        auth={"device_id": "dev123", "key": "WRONG", "salt": "dummysalt1"}
    )
    assert not bad_client.is_connected()

def test_message_exchange(client):
    client.emit("message", {"hello": "world"})
    received = client.get_received()
    assert received  # pastikan ada balasan

