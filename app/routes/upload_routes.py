from fastapi import APIRouter, UploadFile, File
import shutil
import os
import uuid

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

UPLOAD_DIR = "uploads"

# Create folder if not exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def upload_file(
    file: UploadFile = File(...)
):
    # Generate unique filename
    file_ext = file.filename.split(".")[-1]

    unique_name = f"{uuid.uuid4()}.{file_ext}"

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_name
    )

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "filename": unique_name,
        "url": f"/uploads/{unique_name}"
    }