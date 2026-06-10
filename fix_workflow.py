import urllib.request
import json
import os

req = urllib.request.urlopen('http://127.0.0.1:8000/history')
data = json.loads(req.read())
last_key = list(data.keys())[-1]
prompt = data[last_key]['prompt'][2]

for node_id, node in prompt.items():
    if node.get('class_type') == 'XFluxImageEdit':
        node['inputs']['unet_name'] = 'flux-2-klein-base-9b-fp8.safetensors'
        node['inputs']['vae_name'] = 'full_encoder_small_decoder.safetensors'

# Let's also check if it's named something else
    if 'unet_name' in node.get('inputs', {}):
        if 'qwen' in str(node['inputs']['unet_name']):
             node['inputs']['unet_name'] = 'flux-2-klein-base-9b-fp8.safetensors'
    if 'vae_name' in node.get('inputs', {}):
        if 'audio' in str(node['inputs']['vae_name']):
             node['inputs']['vae_name'] = 'full_encoder_small_decoder.safetensors'

out_path = r'C:\Users\Admin\Documents\ComfyUI\user\default\workflows\Flux2_Klein_Fixed.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(prompt, f, indent=2)

print(f'Saved to {out_path}')
