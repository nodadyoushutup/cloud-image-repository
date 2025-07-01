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

### Generate an API key

The server expects an API key for uploads. You can create one using the
`generate_api_key.sh` script:

```bash
./generate_api_key.sh
```

Use the printed key as the value for the `CLOUD_REPOSITORY_APIKEY` environment
variable.

### Simulate an Upload

Use the `simulate_upload.sh` script to send a file to the server, simulating an upload from a GitHub Action. Set the `CLOUD_REPOSITORY_APIKEY` environment variable to the API key expected by the server:

```bash
export CLOUD_REPOSITORY_APIKEY="$(./generate_api_key.sh)"
./simulate_upload.sh path/to/your-image.img
```

The response from the server will be a JSON object containing the path of the uploaded file and the path to a `sha256` file containing the checksum. Both will be located under the `uploads/` directory and can be used as assets for a GitHub release.
