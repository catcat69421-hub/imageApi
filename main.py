from fastapi import FastAPI
from PIL import Image
import requests
from io import BytesIO

app = FastAPI()

@app.get("/")
def home():
    return {"status": "online"}

@app.get("/image")
def image(url: str):

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content)).convert("RGB")
        img = img.resize((32,32))

        pixels = []

        for y in range(img.height):
            row = []

            for x in range(img.width):
                r,g,b = img.getpixel((x,y))
                row.append([r,g,b])

            pixels.append(row)

        return pixels

    except Exception as e:
        return {"error": str(e)}
