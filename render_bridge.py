# Server side of the input-driven render round-trip: detects connected inputs,
# send_syncs the resolved params to the browser, and blocks on a threading.Event
# until the browser POSTs the rendered PNG back to the /sphere_light/result route.

import threading
import uuid

try:
    from server import PromptServer          # available inside ComfyUI
except Exception:                             # standalone test harness
    PromptServer = None

RENDER_EVENT = "sphere_light.render"
RESULT_ROUTE = "/sphere_light/result"

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


def _client_connected():
    # PromptServer.instance.sockets is a dict of sid -> websocket. Non-empty
    # means at least one browser tab is listening. VERIFY the attribute name
    # against your ComfyUI (older builds: .sockets; confirm in a REPL / spike).
    inst = getattr(PromptServer, "instance", None)
    return bool(inst and getattr(inst, "sockets", None))


def render(node_id, params, timeout=30.0):
    if PromptServer is None:
        return None
    run_token = uuid.uuid4().hex
    payload = build_payload(node_id, run_token, params)
    def notify():
        # send_sync is broadcast; the frontend filters by node_id. Safe to call
        # from the execution worker thread (it schedules onto the event loop).
        PromptServer.instance.send_sync(RENDER_EVENT, payload)
    return request_render(node_id, run_token, notify, _client_connected, timeout)


# --- POST route: the browser returns the rendered PNG here ---
if PromptServer is not None:
    @PromptServer.instance.routes.post(RESULT_ROUTE)
    async def _sphere_light_result(request):
        from aiohttp import web
        data = await request.json()          # {node_id, run_token, image}
        ok = deliver(data.get("node_id"), data.get("run_token"), data.get("image"))
        return web.json_response({"ok": ok})
