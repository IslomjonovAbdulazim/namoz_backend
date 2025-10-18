import os
from google.cloud import storage
from google.oauth2 import service_account
from fastapi import UploadFile, HTTPException
from typing import Optional
from app.core.config import settings
import uuid

class GoogleCloudStorage:
    def __init__(self):
        self.client = None
        self.bucket = None
        self._initialize_client()
    
    def _initialize_client(self):
        try:
            if os.path.exists(settings.GOOGLE_CLOUD_KEY_FILE):
                credentials = service_account.Credentials.from_service_account_file(
                    settings.GOOGLE_CLOUD_KEY_FILE
                )
                self.client = storage.Client(
                    credentials=credentials, 
                    project=settings.GOOGLE_CLOUD_PROJECT
                )
                self.bucket = self.client.bucket(settings.GOOGLE_CLOUD_BUCKET)
            else:
                print(f"Warning: Google Cloud key file '{settings.GOOGLE_CLOUD_KEY_FILE}' not found. Storage functionality will be disabled.")
        except Exception as e:
            print(f"Warning: Failed to initialize Google Cloud Storage: {str(e)}")
    
    def _check_client(self):
        if self.client is None or self.bucket is None:
            raise HTTPException(
                status_code=503, 
                detail="Google Cloud Storage is not configured. Please check your credentials."
            )
    
    def upload_file(self, file: UploadFile, folder: str = "uploads") -> str:
        self._check_client()
        try:
            file_extension = file.filename.split(".")[-1] if "." in file.filename else ""
            filename = f"{folder}/{uuid.uuid4()}.{file_extension}"
            
            blob = self.bucket.blob(filename)
            
            file.file.seek(0)
            blob.upload_from_file(file.file, content_type=file.content_type)
            
            blob.make_public()
            
            return blob.public_url
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
    
    def delete_file(self, file_url: str) -> bool:
        self._check_client()
        try:
            blob_name = file_url.split(f"{settings.GOOGLE_CLOUD_BUCKET}/")[-1]
            blob = self.bucket.blob(blob_name)
            blob.delete()
            return True
        except Exception:
            return False

storage_service = GoogleCloudStorage()