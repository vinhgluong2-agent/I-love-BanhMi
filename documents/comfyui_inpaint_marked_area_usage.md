# ComfyUI Inpainting - Marked Area Only

Files:

- `comfyui_inpaint_marked_area_workflow.json`: load this in the ComfyUI interface.
- `comfyui_inpaint_marked_area_api.json`: API prompt version for `POST /prompt`.

How to use in ComfyUI:

1. Open ComfyUI and load `documents/comfyui_inpaint_marked_area_workflow.json`.
2. In the `LoadImage` node, choose the base image you want to edit.
3. Right-click the loaded image and choose `Open in MaskEditor`.
4. Paint the area you want to change. The painted/white mask area is the only area the workflow will edit.
5. Edit the positive prompt in the first `CLIPTextEncode` node. Put the requested change at the start of the prompt.
6. Queue the prompt.

Notes:

- The workflow uses `flux1-Fill-Dev_FP8.safetensors`, `InpaintModelConditioning`, `GrowMask`, `FeatherMask`, then composites the result back over the original image with the same feathered mask. This helps keep unmarked areas unchanged.
- `GrowMask` is set to `16` and `FeatherMask` is set to `16` on all sides. Increase these if the edited edge looks too sharp. Lower them if the edit bleeds too far outside the marked area.
- Use `denoise` around `0.65-0.80` for smaller realistic fixes. Use `0.85-0.95` when the marked area should change strongly.
- If the workflow says a model is missing, check these nodes: `UNETLoader` should use `flux1-Fill-Dev_FP8.safetensors`, `DualCLIPLoader` should use `t5xxl_fp8_e4m3fn.safetensors` and `clip_l.safetensors`, and `VAELoader` should use `ae.safetensors`.
