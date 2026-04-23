from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from rembg import remove, new_session
import io

app = FastAPI(title="Background Remover", version="1.0")

# Pre-load model on startup (faster first request)
session = new_session("u2net")

@app.get("/")
def health():
    return {"status": "ok", "service": "rembg background remover"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    contents = await file.read()
    output = remove(contents, session=session)
    
    return Response(
        content=output,
        media_type="image/png",
        headers={"Content-Disposition": f"attachment; filename=nobg_{file.filename}"}
    )
