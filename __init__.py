import torch
import numpy as np
from PIL import Image
import io, base64

class SphereLightNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "rotation":  ("FLOAT", {"default": 0.0,  "min": -180, "max": 180, "step": 1,   "display": "slider"}),
                "elevation": ("FLOAT", {"default": 45.0, "min": 5,    "max": 85,  "step": 1,   "display": "slider"}),
                "intensity": ("FLOAT", {"default": 1.5,  "min": 0.2,  "max": 3.0, "step": 0.1, "display": "slider"}),
                "render_b64": ("STRING", {"default": "", "multiline": False}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("render",)
    FUNCTION = "execute"
    CATEGORY = "render/3d"
    OUTPUT_NODE = False

    def execute(self, rotation, elevation, intensity, render_b64):
        if render_b64 and render_b64.startswith("data:image"):
            try:
                header, data = render_b64.split(",", 1)
                img_bytes = base64.b64decode(data)
                img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
                img = img.resize((1024, 1024), Image.LANCZOS)
            except Exception as e:
                print(f"[SphereLightNode] Error: {e}")
                img = Image.new("RGB", (1024, 1024), (138, 138, 138))
        else:
            img = Image.new("RGB", (1024, 1024), (138, 138, 138))

        arr = np.array(img).astype(np.float32) / 255.0
        tensor = torch.from_numpy(arr).unsqueeze(0)
        return (tensor,)


NODE_CLASS_MAPPINGS = {"SphereLightNode": SphereLightNode}
NODE_DISPLAY_NAME_MAPPINGS = {"SphereLightNode": "🔆 Sphere Light Render"}
WEB_DIRECTORY = "./js"