# Server side of the input-driven render round-trip. The heavy ComfyUI wiring
# (route, send_sync, event wait) is added in later tasks; the pure helpers below
# import nothing beyond threading.

import threading

# (node_id, run_token) -> {"event": Event, "image": None}
_pending = {}
_lock = threading.Lock()


def is_driven(prompt, node_id, param_names):
    """True if any of param_names is a connected input (a [upstream_id, slot]
    link) for this node in the prompt graph, rather than a literal widget value."""
    try:
        inputs = prompt[str(node_id)]["inputs"]
    except (KeyError, TypeError):
        return False
    return any(isinstance(inputs.get(name), list) for name in param_names)


def build_payload(node_id, run_token, params):
    return {"node_id": str(node_id), "run_token": run_token, "params": params}


def request_render(node_id, run_token, notify, client_connected, timeout=30.0):
    key = (str(node_id), run_token)
    event = threading.Event()
    with _lock:
        _pending[key] = {"event": event, "image": None}
    try:
        if not client_connected():
            return None            # no browser to render -> caller falls back
        notify()                   # tell the browser to render + post back
        if not event.wait(timeout):
            return None            # backstop: frozen/absent tab
        with _lock:
            return _pending[key]["image"]
    finally:
        with _lock:
            _pending.pop(key, None)


def deliver(node_id, run_token, image):
    key = (str(node_id), run_token)
    with _lock:
        entry = _pending.get(key)
        if entry is None:
            return False           # stale/unknown token
        entry["image"] = image
        entry["event"].set()
        return True
