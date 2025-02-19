from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import requests
from PIL import Image
import io
import base64
from PIL import PngImagePlugin


sd_url = "http://127.0.0.1:7860"


def generate_image(prompt):
   
    # 构建请求负载
    payload = {
        "prompt": prompt,
        "steps": 15,
        "width": 256,
        "height":256
    }

    # 向 Stable Diffusion Web UI 发送请求生成图像
    response = requests.post(url=f'{sd_url}/sdapi/v1/txt2img', json=payload)
    r = response.json()

    if 'images' in r and r['images']:
        # 获取第一个生成的图像
        image_base64 = r['images'][0].split(",", 1)[0]
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_bytes))

        # 获取图像的 PNG 信息
        png_payload = {
            "image": "data:image/png;base64," + r['images'][0]
        }
        response2 = requests.post(url=f'{sd_url}/sdapi/v1/png-info', json=png_payload)
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))

        # 将图像保存到内存中
        img_io = io.BytesIO()
        image.save(img_io, 'PNG', pnginfo=pnginfo)
        img_io.seek(0)

        # 返回图像文件
        return img_io
    
    else:
        return None
    

