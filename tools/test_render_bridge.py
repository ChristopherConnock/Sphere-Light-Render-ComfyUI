import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import render_bridge as rb

# is_driven: a link is a [id, slot] list; a literal is a scalar.
PROMPT = {"7": {"inputs": {
    "heading": ["3", 0],          # connected
    "intensity": 1.5,             # literal widget value
    "city": "Austin, TX",
}, "class_type": "SphereLightSunCityNode"}}

assert rb.is_driven(PROMPT, "7", ["heading", "intensity"]) is True   # heading is a link
assert rb.is_driven(PROMPT, "7", ["intensity", "city"]) is False     # all literals
assert rb.is_driven(PROMPT, 7, ["heading"]) is True                  # int node_id coerced
assert rb.is_driven(PROMPT, "999", ["heading"]) is False             # missing node
assert rb.is_driven({}, "7", ["heading"]) is False                   # empty prompt

p = rb.build_payload("7", "tok1", {"heading": 90})
assert p == {"node_id": "7", "run_token": "tok1", "params": {"heading": 90}}, p

import threading, time

# Success: a "browser" thread delivers the image; request_render returns it.
def deliver_later(node_id, token, image, delay):
    time.sleep(delay)
    rb.deliver(node_id, token, image)

t = threading.Thread(target=deliver_later, args=("7", "tokA", "data:image/png;base64,AAAA", 0.05))
t.start()
got = rb.request_render("7", "tokA", notify=lambda: None, client_connected=lambda: True, timeout=2.0)
t.join()
assert got == "data:image/png;base64,AAAA", got

# No client connected -> immediate None, notify never called.
called = []
none1 = rb.request_render("7", "tokB", notify=lambda: called.append(1), client_connected=lambda: False, timeout=2.0)
assert none1 is None and called == [], (none1, called)

# Timeout (nobody delivers) -> None.
t0 = time.time()
none2 = rb.request_render("7", "tokC", notify=lambda: None, client_connected=lambda: True, timeout=0.2)
assert none2 is None, none2
assert time.time() - t0 < 1.0  # returned promptly at the timeout, not hung

# deliver for an unknown token is a no-op returning False.
assert rb.deliver("7", "no-such-token", "x") is False

print("test_render_bridge: OK")
