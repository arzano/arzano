from fastapi import FastAPI, Request, Response, status
from PIL import Image, ImageDraw
from io import BytesIO
from starlette.responses import StreamingResponse
import os, random

app = FastAPI()

def get_image():
    img = Image.open("./images/" + random.choice(os.listdir("./images/")))
    return img


def serve_pil_image(img):
    buf = BytesIO()
    img.save(buf, "png")
    buf.seek(0)
    headers = {"Cache-Control": "max-age=0, no-cache, no-store, must-revalidate"}
    return StreamingResponse(buf, headers=headers, media_type="image/png")


def is_image_request(request: Request) -> bool:
    headers = request.headers
    header_sec_fetch_dest = headers["sec-fetch-dest"] if "sec-fetch-dest" in headers else ""
    header_accept = headers["accept"] if "accept" in headers else ""
    result = True if header_sec_fetch_dest == "image" else "text/html" not in header_accept
    return result


@app.get("/")
def api(request: Request):
    if is_image_request(request=request):
        img = get_image()
        return serve_pil_image(img)
    else:
        return Response(status_code=status.HTTP_200_OK)

