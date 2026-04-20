
from fastapi import APIRouter, UploadFile
import shutil
import uuid

router = APIRouter()

@router.post("/product-image")
async def upload_image(file: UploadFile):

    filename = f"{uuid.uuid4()}.jpg"
    path = f"uploads/{filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "url": f"http://localhost:8000/uploads/{filename}"
    }
