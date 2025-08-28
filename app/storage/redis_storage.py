import redis, json

# koneksi redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
REDIS_KEY = "connected_devices"


# ================= STORAGE HELPERS ===============

def _load_all():
    """Ambil semua connected_devices dari Redis (return dict)."""
    raw = redis_client.get(REDIS_KEY)
    return json.loads(raw) if raw else {}


def _save_all(data: dict):
    """Simpan dict ke Redis."""
    redis_client.set(REDIS_KEY, json.dumps(data))


def save_device(device_id: str, sid: str, client_type: str):
    devices = _load_all()
    if device_id not in devices:
        devices[device_id] = {}
    devices[device_id][sid] = client_type
    _save_all(devices)
    print(f"INFO: save_device → {device_id} : {sid} ({client_type})")


def remove_device(device_id: str, sid: str):
    devices = _load_all()
    if device_id in devices and sid in devices[device_id]:
        del devices[device_id][sid]
        if not devices[device_id]:
            del devices[device_id]
        _save_all(devices)
        print(f"INFO: remove_device → {sid} removed from {device_id}")


def get_room_members(device_id: str):
    devices = _load_all()
    return devices.get(device_id, {})


def find_device_by_sid(sid: str):
    devices = _load_all()
    for device_id, members in devices.items():
        if sid in members:
            return device_id, members[sid]
    return None, None

def save_payload(device_id: str, payload: dict, sid: str):
    """
    Simpan payload terbaru dari IoT ke Redis sesuai device_id.
    Validasi: hanya SID yang terdaftar sebagai IoT yang boleh menyimpan.
    """
    devices = _load_all()

    if device_id not in devices:
        print(f"WARN: Device {device_id} not found in Redis")
        return False

    # cek apakah sid ini terdaftar sebagai IoT
    members = devices[device_id]
    if members.get(sid) != "iot":
        print(f"WARN: SID {sid} is not registered as IoT for device {device_id}")
        return False

    # simpan payload terakhir
    devices[device_id]["last_payload"] = payload
    _save_all(devices)

    print(f"INFO: Payload saved for {device_id} by SID {sid} → {payload}")
    return True
