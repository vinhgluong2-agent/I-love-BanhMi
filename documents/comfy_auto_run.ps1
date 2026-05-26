$json = @"
{
  "3": {
    "inputs": {
      "seed": $(Get-Random -Minimum 100000 -Maximum 999999999),
      "steps": 35,
      "cfg": 6.5,
      "sampler_name": "dpmpp_2m_sde",
      "scheduler": "karras",
      "denoise": 1.0,
      "model": ["4", 0],
      "positive": ["10", 0],
      "negative": ["7", 0],
      "latent_image": ["5", 0]
    },
    "class_type": "KSampler"
  },
  "4": {
    "inputs": {
      "ckpt_name": "v1-5-pruned-emaonly.safetensors"
    },
    "class_type": "CheckpointLoaderSimple"
  },
  "5": {
    "inputs": {
      "width": 960,
      "height": 512,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage"
  },
  "6": {
    "inputs": {
      "text": "raw photo, ultra-realistic architectural photography, empty space transformed into a bustling gritty industrial warehouse cafe, beautiful grey cement floor, massive solid concrete bar counter on the right side, corrugated metal wainscoting, exposed matte black ceiling, warm yellow hanging string lights, eclectic vintage leather sofas, cinder block tables, 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT4, highly detailed, photorealistic, architectural digest, cinematic lighting, dramatic shadows",
      "clip": ["4", 1]
    },
    "class_type": "CLIPTextEncode"
  },
  "7": {
    "inputs": {
      "text": "drawing, painting, illustration, cartoon, 3d render, lowres, bad architecture, deformed structures, ugly, messy lines, bad proportions, bad perspective, text, watermark, worst quality, low quality, normal quality, jpeg artifacts, blurry",
      "clip": ["4", 1]
    },
    "class_type": "CLIPTextEncode"
  },
  "8": {
    "inputs": {
      "samples": ["3", 0],
      "vae": ["4", 2]
    },
    "class_type": "VAEDecode"
  },
  "9": {
    "inputs": {
      "filename_prefix": "Auto_Cafe_SketchUp_Ultra",
      "images": ["8", 0]
    },
    "class_type": "SaveImage"
  },
  "10": {
    "inputs": {
      "strength": 0.65,
      "start_percent": 0.0,
      "end_percent": 0.8,
      "positive": ["6", 0],
      "negative": ["7", 0],
      "control_net": ["11", 0],
      "image": ["13", 0]
    },
    "class_type": "ControlNetApplyAdvanced"
  },
  "11": {
    "inputs": {
      "control_net_name": "control_v11p_sd15_canny.pth"
    },
    "class_type": "ControlNetLoader"
  },
  "12": {
    "inputs": {
      "image": "sketchup_base.png",
      "upload": "image"
    },
    "class_type": "LoadImage"
  },
  "13": {
    "inputs": {
      "low_threshold": 0.1,
      "high_threshold": 0.3,
      "image": ["12", 0]
    },
    "class_type": "Canny"
  }
}
"@

$payload = @{
    prompt = $json | ConvertFrom-Json
}

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/prompt" -Method Post -Body ($payload | ConvertTo-Json -Depth 10) -ContentType "application/json"
Write-Output "Prompt queued with ID: $($response.prompt_id)"
