# Sphere-Light-Render-ComfyUI
Widget to tell Flux 2 Klein 9B where the sun light comes from. To be used with Sun_direction_Lora for Flux2Klein

## Install

Clone into your `ComfyUI/custom_nodes/`:

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/eric-venti-seeds/Sphere-Light-Render-ComfyUI.git
```

Restart ComfyUI. No additional Python dependencies for the core node.

## Quick start

Download the Lora from here:

https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B



The Node renders a 1024 x 1024 image as reference for the LoRA to understand where the light comes from

<img width="484" height="720" alt="sphere" src="https://github.com/user-attachments/assets/581bfc3c-61a6-48da-9b25-89275a2bee10" />

<img width="1288" height="770" alt="Sphere_Light_Render_ComfyUI_Node" src="https://github.com/user-attachments/assets/3e6a27a6-2eca-442c-9f4f-91a674857f89" />

## Time of day

Set `sun_mode` to `date/time` to position the light from a real sun position.
Enter a `location` ("City, State" for the US, or "City, Country" elsewhere — from
a bundled offline list of cities over ~15k population), the date/time, and the
compass `heading` the camera faces. Timezone and daylight-saving are handled
automatically. Places not in the list: switch back to `manual`, or use a nearby
listed city. Rebuild the city list with `python tools/build_cities.py`.
