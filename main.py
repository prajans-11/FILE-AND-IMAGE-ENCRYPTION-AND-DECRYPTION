from fastapi import FastAPI, Form, Request, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from PIL import Image
import io
import base64

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

def is_base64_encoded(text):
    try:
        base64_bytes = base64.b64decode(text)
        return True
    except base64.binascii.Error:
        return False

def decode_image(encoded_image):
    try:
        image_data = base64.b64decode(encoded_image.encode("utf-8"))
        image = Image.open(io.BytesIO(image_data))
        return image
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Image Data")

@app.get("/")
def front(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/encrypt-text")
def encrypt_text(request: Request, key: str = Form(...), text: str = Form(...), but: str = Form(...)):
    if but == 'encrypt':
        if key == "1234":
            encode_message = text.encode("utf-8")
            base64_bytes = base64.b64encode(encode_message)
            encrypted = base64_bytes.decode("utf-8")
            return templates.TemplateResponse("index.html", {"request": request, "result": encrypted})
        else:
            return templates.TemplateResponse("index.html", {"request": request})
    else:
        if key == "1234":
            try:
                decode_message = base64.b64decode(text)
                decrypted = None

                encodings = ["utf-8", "latin1", "iso-8859-1"]
                for encoding in encodings:
                    try:
                        decrypted = decode_message.decode(encoding)
                        break
                    except UnicodeDecodeError:
                        continue

                if decrypted is None:
                    error_message = "Already Decrypted"
                    return templates.TemplateResponse("index.html", {"request": request, "result": error_message})

                return templates.TemplateResponse("index.html", {"request": request, "result": decrypted})
            except Exception as e:
                error_message = "Decryption failed"
                return templates.TemplateResponse("index.html", {"request": request, "result": error_message})
        elif not key:
            error_message = "Please provide the decryption password."
            return templates.TemplateResponse("index.html", {"request": request, "result": error_message})
        else:
            error_message = "Invalid Password"
            return templates.TemplateResponse("index.html", {"request": request, "result": error_message})

@app.post("/encrypt-decrypt-image")
async def encrypt_decrypt_image(request: Request, key1: str = Form(...), image: UploadFile = Form(...), but: str = Form(...), text1: str = Form("Nil")):
    if but == 'encrypt':
        if key1 == "1234":
            image_data = await image.read()
            encoded_image = base64.b64encode(image_data).decode("utf-8")
            return templates.TemplateResponse("index.html", {"request": request, "result1": encoded_image})
        elif not key1:
            error_message = "Please provide a password."
            return templates.TemplateResponse("index.html", {"request": request, "result1": error_message})
        else:
            error_message = "Invalid Password"
            return templates.TemplateResponse("index.html", {"request": request, "result1": error_message})
    else:
        if key1 == "1234":
            try:
                image = decode_image(text1)
                img_bytes = io.BytesIO()
                image.save(img_bytes, format="PNG")
                img_bytes.seek(0)
                decrypted_image_path = "decrypted_image.png"
                with open(decrypted_image_path, "wb") as f:
                    f.write(img_bytes.read())
                return templates.TemplateResponse("index.html", {"request": request, "result1": "Image decrypted and saved."})
            except Exception as e:
                raise HTTPException(status_code=400, detail="Image Decryption Failed")
        elif not key1:
            raise HTTPException(status_code=400, detail="Input Password")
        else:
            raise HTTPException(status_code=401, detail="Invalid Password")
