# Libraries
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
import json
import os
from datetime import datetime
import logging
from Utils.fileUtils import extract_and_transform_from_pdf_for_llm

# Constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
INPUTFILE_STORAGE_DIRECTORY = "./uploaded_files"
OUTPUTFILE_STORAGE_DIRECTORY = "./generated_files"

# Ensure the directory exists
os.makedirs(INPUTFILE_STORAGE_DIRECTORY, exist_ok=True)
os.makedirs(OUTPUTFILE_STORAGE_DIRECTORY, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/uploadfile/")
async def pdfScanner(file: UploadFile = File(...)):
    logger.info(f"Received file upload request: {file.filename}")
    # Read the file content
    content = await file.read()

    # Check the file type
    if file.content_type != 'application/pdf':
        logger.error(f"Invalid file type: {file.content_type} for file: {file.filename}")
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
    # Limit file size
    if(len(content)>MAX_FILE_SIZE):
        logger.error(f"File size exceeds the 10MB limit: {file.filename} ({len(content)} bytes)")
        raise HTTPException(status_code=413, detail="File size exceeds the 10MB limit")
    
    # Read the file content and check the size
    content = await file.read()

    # Save the uploaded file
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    uploaded_filename = f"{timestamp}_{file.filename}"
    uploaded_filepath = os.path.join(INPUTFILE_STORAGE_DIRECTORY, uploaded_filename)

    with open(uploaded_filepath, "wb") as f:
        f.write(content)

    logger.info(f"Saved Uploaded file as: {uploaded_filepath}")

    # Initialize the payload
    payload = {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "file_path": uploaded_filepath
    }
    # Text Extraction Code
    result = extract_and_transform_from_pdf_for_llm(payload)

    return JSONResponse(content=result)
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
