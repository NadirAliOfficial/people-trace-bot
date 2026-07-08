import cloudinary
from cloudinary.uploader import upload
from config.config_manager import (
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
    CLOUDINARY_CLOUD_NAME,
)
from typing import Dict


# Configuring Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
)


# Custom CloudinaryError class to raise detailed exceptions
class CloudinaryError(Exception):
    def __init__(self, message: str, response: Dict = None):
        self.message = message
        self.response = response
        super().__init__(message)


async def upload_image(image: str):
    try:
        upload_result = upload(image)
        file_url = upload_result["secure_url"]
        print(f"Uploaded Image URL: {file_url}")
        return file_url
    except cloudinary.exceptions.Error as e:
        print(f"Cloudinary error: {e}")
        raise CloudinaryError("Error uploading image to Cloudinary.", e.response)


async def upload_video(file_path: str):
    """Upload the video file to Cloudinary."""
    try:
        # Cloudinary upload for video
        upload_result = upload(
            file_path,
            resource_type="video",  # Specifies the upload type as video
            folder="proofs",  # Optional: Upload to a specific folder
            public_id=file_path,  # Optional: Use the file's path as its public ID
        )

        print(f"Cloudinary upload result: {upload_result}")


        # Return the secure URL for the uploaded video
        file_url = upload_result["secure_url"]
        print(f"Uploaded Video URL: {file_url}")
        return file_url
    except cloudinary.exceptions.Error as e:
        # Handle any errors from Cloudinary during the upload process
        print(f"Cloudinary upload error: {e}")
        raise CloudinaryError("Error uploading video to Cloudinary.", e.response)
