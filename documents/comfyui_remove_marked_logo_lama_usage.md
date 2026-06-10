# ComfyUI Marked Logo Remover

Use this workflow when you want to remove a marked logo, sticker, decal, printed text, or small object and fill the area with the surrounding product surface.

Files:

- `comfyui_remove_marked_logo_lama_workflow.json`: load this in the ComfyUI interface.
- `comfyui_remove_marked_logo_lama_api.json`: API prompt version.

How to use:

1. Load `documents/comfyui_remove_marked_logo_lama_workflow.json` in ComfyUI.
2. Choose the source image in `LoadImage`.
3. Right-click the image and choose `Open in MaskEditor`.
4. Paint over the whole logo, including all black outline, shadow, and small leftover marks.
5. Queue the workflow.

Tuning:

- `GrowMask` default is `18`, because logo outlines often leave dark pixels if the mask is too tight.
- Lower `GrowMask` to `8-12` if the edit removes too much nearby cup detail.
- Raise `GrowMask` to `22-30` if any part of the logo remains.
- `FeatherMask` default is `4` for a cleaner edge. Raise to `8-12` if the boundary looks harsh.

This workflow uses `LaMaInpaint`, not prompt-based diffusion. It is better for logo removal because it will not hallucinate a new logo from nearby examples.
