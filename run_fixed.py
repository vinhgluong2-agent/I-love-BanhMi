import urllib.request
import json

req = urllib.request.urlopen('http://127.0.0.1:8000/history')
data = json.loads(req.read())
last_key = list(data.keys())[-1]
prompt = data[last_key]['prompt'][2]

for node_id, node in prompt.items():
    if 'unet_name' in node.get('inputs', {}):
        if 'qwen' in str(node['inputs']['unet_name']):
             node['inputs']['unet_name'] = 'flux-2-klein-base-9b-fp8.safetensors'
    if 'vae_name' in node.get('inputs', {}):
        if 'audio' in str(node['inputs']['vae_name']):
             node['inputs']['vae_name'] = 'full_encoder_small_decoder.safetensors'

payload = json.dumps({'prompt': prompt}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:8000/prompt', data=payload, headers={'Content-Type': 'application/json'})
res = urllib.request.urlopen(req)
print(res.read().decode('utf-8'))
