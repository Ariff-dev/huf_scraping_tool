import os
import tempfile
import requests
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

# Configure Cloudinary from env vars
# Add to your .env:
#   CLOUDINARY_CLOUD_NAME=your_cloud_name
#   CLOUDINARY_API_KEY=your_api_key
#   CLOUDINARY_API_SECRET=your_api_secret
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)


def upload_image_from_url(image_url: str, folder: str = "general") -> dict:
    """
    Downloads an image from a URL and uploads it to Cloudinary.

    Args:
        image_url: Public URL of the image to download.
        folder:    Destination folder in Cloudinary (e.g. 'artistas', 'canciones').
                   Defaults to 'general'. Can be set dynamically per call.

    Returns:
        dict with:
          - public_id  (str)  → store this in Supabase
          - secure_url (str)  → ready-to-use CDN URL
          - width, height, format, ...

    Raises:
        ValueError: if the URL can't be downloaded or Cloudinary rejects the upload.
    """
    # 1. Download image to a temp file (works on any OS / server)
    response = requests.get(image_url, timeout=15)
    if not response.ok:
        raise ValueError(f"Failed to download image ({response.status_code}): {image_url}")

    content_type = response.headers.get("Content-Type", "image/jpeg")
    extension = content_type.split("/")[-1].split(";")[0]  # e.g. 'jpeg', 'png', 'webp'

    with tempfile.NamedTemporaryFile(suffix=f".{extension}", delete=False) as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    # 2. Upload to Cloudinary
    try:
        result = cloudinary.uploader.upload(
            tmp_path,
            folder=folder,
            resource_type="image",
            overwrite=False,
            unique_filename=True,
        )
    finally:
        # Always clean up the temp file regardless of upload success
        os.remove(tmp_path)

    return {
        "public_id": result["public_id"],
        "secure_url": result["secure_url"],
        "width": result.get("width"),
        "height": result.get("height"),
        "format": result.get("format"),
    }
