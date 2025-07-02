# GitHub Action Integration Guide

This document describes how to interact with the cloud-image-repository from a GitHub Action. The action uploads an image file using `curl` and stores the response for use in your release workflow.

## Uploading an Image

1. Obtain an API key using `generate_api_key.sh` and configure it as a secret named `CLOUD_REPOSITORY_APIKEY` in your repository.
2. Use `curl` to POST the image with the required header:

```bash
curl -H "CLOUD-REPOSITORY-APIKEY: ${{ secrets.CLOUD_REPOSITORY_APIKEY }}" \
     -F "file=@path/to/image.img" \
     https://your-repo-host.tld/upload
```

The server returns JSON similar to:

```json
{
  "path": "files/cloud-image-x86-64-jammy-0.1.33.img",
  "sha256_file": "files/cloud-image-x86-64-jammy-0.1.33.img.sha256",
  "sha256": "..."
}
```

`path` and `sha256_file` are relative URLs that you can attach to your release assets or include in the release notes.

## Example GitHub Action Step

```yaml
- name: Upload image to repository
  id: upload_img
  run: |
    response=$(curl -s -H "CLOUD-REPOSITORY-APIKEY: ${{ secrets.CLOUD_REPOSITORY_APIKEY }}" \
                   -F "file=@${{ steps.build.outputs.image }}" \
                   https://your-repo-host.tld/upload)
    echo "response=$response" >> "$GITHUB_OUTPUT"
```

Later steps in the workflow can access `${{ steps.upload_img.outputs.response }}` and parse `path` and `sha256_file` to link the assets in a GitHub release.

This setup allows automation of releases that reference images stored in this repository without embedding large files directly in your main repository.
