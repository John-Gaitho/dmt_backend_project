from fastapi import APIRouter, UploadFile, File, HTTPException
import cloudinary
import cloudinary.uploader

from app.config import settings

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

# =========================
# CLOUDINARY CONFIG
# =========================

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

# =========================
# UPLOAD IMAGE
# =========================

@router.post("/")
async def upload_file(
    file: UploadFile = File(...)
):
    try:
        result = cloudinary.uploader.upload(
            file.file,
            folder="dmt_uploads"
        )

        return {
            "filename": result["public_id"],
            "url": result["secure_url"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )