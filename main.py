from fastapi import FastAPI
from PIL import Image
import requests
from io import BytesIO

app = FastAPI()

# ✔ Health check (Render + browser test)
@app.get("/")
def home():
    return {"status": "online"}

# ✔ Image → pixel converter API
@app.get("/image")
def image(url: str):

    try:
        # Download image safely (fixes Imgur 429 issue)
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()

        # Open image
        img = Image.open(BytesIO(r.content)).convert("RGB")

        # Resize so Roblox doesn't lag
        img = img.resize((32, 32))

        pixels = []

        # Convert to RGB grid
        for y in range(img.height):
            row = []
            for x in range(img.width):
                r, g, b = img.getpixel((x, y))
                row.append([r, g, b])
            pixels.append(row)

        return pixels

    except Exception as e:
        # Return error instead of crashing server
        return {"error": str(e)}
