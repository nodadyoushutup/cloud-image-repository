# cloud-image-repository

An image repository for cloud images.

## Flask App

This repository includes a simple Flask application that can store uploaded image files and provide download links. To run the server locally:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

The application listens on port `5000` by default. Visit `http://localhost:5000/` to see the list of uploaded files and use the upload form.

### Simulate an Upload

Use the `simulate_upload.sh` script to send a file to the server, simulating an upload from a GitHub Action. The script requires a `GH_TOKEN` environment variable which will be sent as the `GITHUB_TOKEN` header:

```bash
export GH_TOKEN=your-token-value
./simulate_upload.sh path/to/your-image.img
```

The uploaded file will be saved in the `uploads/` directory and listed on the homepage.
