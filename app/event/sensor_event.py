from flask import request
from flask_socketio import join_room, leave_room, disconnect
from app.utils.extension import socketio
from app.storage.redis_storage import (
    save_device, remove_device, get_room_members,
    find_device_by_sid, save_payload
)

from flask import request

# =============== AUTH HELPER =================

def login(device_id, client_type):
    """
    Validasi device_id dan tipe client.
    """
    if not device_id or client_type not in ("iot", "frontend"):
        print(f"WARN: Unauthorized connection attempt: {request.sid}")  # type: ignore
        return False
    
    # TODO: validasi device_id dari MongoDB
    
    return True

####################################################

@socketio.on("connect")
def handle_connect(auth):
    device_id = auth.get("device_id") if auth else None
    client_type = auth.get("client_type") if auth else None

    if not login(device_id, client_type):
        return False

    members = get_room_members(device_id)

    if client_type == "iot":
        existing_iots = [sid for sid, ctype in members.items() if ctype == "iot"]
        if existing_iots:
            for sid in list(members.keys()):
                disconnect(sid)
            remove_device(device_id, request.sid)
            return False

    if client_type == "frontend":
        has_iot = any(ctype == "iot" for ctype in members.values())
        if not has_iot:
            disconnect(request.sid)
            return False

    save_device(device_id, request.sid, client_type)
    join_room(device_id)

    socketio.emit("message", {
        "msg": f"{client_type.capitalize()} for {device_id} authenticated"
    }, to=request.sid)


@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    device_id, client_type = find_device_by_sid(sid)

    if not device_id:
        return

    if client_type == "iot":
        members = get_room_members(device_id)
        for member_sid in list(members.keys()):
            disconnect(member_sid)
        from app.storage.redis_storage import _load_all, _save_all
        devices = _load_all()
        if device_id in devices:
            del devices[device_id]
            _save_all(devices)
    else:
        remove_device(device_id, sid)
        leave_room(device_id)


@socketio.on("iot_data")
def handle_iot_data(data):
    device_id = data.get("device_id")
    payload = data.get("payload")
    members = get_room_members(device_id)
    if not device_id or not members:
        return

    _, client_type = find_device_by_sid(request.sid)
    if client_type != "iot":
        return

    # TODO: validasi payload sesuai dari model database
    
    if save_payload(device_id, payload, request.sid):
        socketio.emit("iot_update", {"device_id": device_id, "payload": payload}, to=device_id)


@socketio.on("message")
def handle_message(data):
    device_id, client_type = find_device_by_sid(request.sid)
    socketio.emit("message", {
        "status": "ok",
        "reply": f"Server received from {client_type}: {data}"
    }, to=request.sid)
