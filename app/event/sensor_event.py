from flask import request
from flask_socketio import SocketIO, join_room, leave_room, disconnect

from app.utils.helpers import success_response
from app.utils.extension import socketio

# Simpan mapping device_id -> sid
connected_devices = {}


def login(device_id, key, salt):
    my_dummy_data = {
        'key': 'dummykey1',
        'salt':'dummysalt1'
    }
    
    if key != my_dummy_data["key"] or salt != my_dummy_data["salt"] or not device_id:
        print(f"Unauthorized connection attempt: {request.sid}") # type: ignore
        return False  
    else:
        return True


@socketio.on("connect")
def handle_connect(auth):
    """
    Saat client mencoba connect, auth diambil dari handshake.
    Kalau tidak valid, return False => otomatis ditolak.
    """
    device_id = auth.get("device_id") if auth else None
    key = auth.get("key") if auth else None
    salt = auth.get("salt") if auth else None

    if not login(device_id, key, salt):
        return False # tolak koneksi

    # Simpan mapping device -> sid
    connected_devices[device_id] = request.sid # type: ignore

    # Join room sesuai device_id
    join_room(device_id)

    print(f"Authorized client connected: {device_id} ({request.sid}) on Room (R_{device_id})") # type: ignore
    socketio.emit("message", {
        "msg": f"Device {device_id} authenticated",
        "room": f"R_{device_id}"
    }, to=device_id)


@socketio.on("disconnect")
def handle_disconnect():
    """
    Hapus sid dari mapping kalau putus.
    """
    sid = request.sid # type: ignore
    device_id = None

    for d, s in list(connected_devices.items()):
        if s == sid:
            device_id = d
            del connected_devices[d]
            break

    print(f"Client disconnected: {sid} (device: {device_id})")
    leave_room(sid)


@socketio.on("message")
def handle_message(data):
    """
    Hanya client yang sudah lewat connect (dan auth valid) bisa sampai sini.
    """
    print(f"Received from {request.sid}:", data) # type: ignore
    socketio.emit("message", {
        "status": "ok",
        "reply": f"Server received: {data}"
    }, to=request.sid) # type: ignore
