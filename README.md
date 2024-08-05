---

# FastAPI File Upload Application

## Overview

This FastAPI application allows users to upload PDF files. It validates the file type, checks the size, saves the uploaded file to a local directory, and generates a JSON file containing metadata about the uploaded file. The application returns a JSON response with file details and a URL to the saved file.

## Features

- Accepts PDF file uploads
- Validates file type and size (maximum of 10MB)
- Saves uploaded files and JSON metadata to specified directories
- Returns a JSON response with file information and a file URL

## Prerequisites

- Python 3.7 or higher
- [pip](https://pip.pypa.io/en/stable/)

## Setup

### 1. Clone the Repository

```bash
git clone [https://github.com/krypc-code/KrypcTCLAI](https://github.com/krypc-code/KrypcTCLAI.git)
cd fastapi-file-upload
```

### 2. Create a Virtual Environment (Optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Logging (Optional)

The logging configuration is set up in the application code. If you need custom logging configuration, modify the `logging.basicConfig` parameters in `app.py`.

### 5. Set the secrets in .env file

Refer to my copy of .env.

### 6. Run the Application Locally

```bash
uvicorn app:app --reload
```

The application will be accessible at `http://127.0.0.1:8000`.

### 6. Run Tests (Optional)

To run tests, ensure you have `pytest` installed and run:

```bash
pytest
```

## Production Deployment

For production deployment, you might want to use a production-ready ASGI server and configure environment variables. Here’s an example of deploying with `gunicorn` and `uvicorn`:

1. **Install Gunicorn**

   ```bash
   pip install gunicorn
   ```

2. **Run Gunicorn with Uvicorn Workers**

   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
   ```

   - `-w 4`: Number of worker processes (adjust based on your server's CPU cores).
   - `-k uvicorn.workers.UvicornWorker`: Use Uvicorn as the worker class for Gunicorn.

### Configuration for Production

- **Set Environment Variables**: You can set environment variables for configuration, such as logging levels or file paths.
- **Use a Reverse Proxy**: For a production environment, it’s recommended to use a reverse proxy like Nginx or Apache to handle HTTP requests and forward them to your FastAPI application.

### Example Nginx Configuration

Here’s a basic Nginx configuration to proxy requests to the FastAPI application:

```nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## API Endpoints

### POST /uploadfile/

**Description**: Upload a PDF file.

**Request**: Multipart form-data with file.

**Response**: JSON object containing file information and file URL.


```

## Troubleshooting

- **File Size Exceeds Limit**: Ensure the file size is within the 10MB limit.
- **Invalid File Type**: Only PDF files are accepted.
- **Directory Permissions**: Ensure the application has write permissions for the upload directories.


## Contributing

Feel free to fork the repository and submit pull requests. Ensure that you follow the project's coding style and include tests for any new features.

## Contact

For any questions or issues, please contact someone @krypc.

---
