# gdrive-core

A minimal and functional Google Drive API wrapper for Python. Easily perform Google Drive file operations like upload, download, list, delete, and manage metadata with an intuitive class-based interface.

## Features

- **Simple Authentication**: Easy setup with `credentials.json`.
- **File Management**: Upload, download, list, and delete files effortlessly.
- **Folder Management**: Create folders and organize files.
- **Custom Metadata**: Add and manage arbitrary custom properties to files.
- **Batch Operations**: Delete multiple files at once.
- **OOP Interface**: Interact with Google Drive through a clean class-based API.

## Installation

Install the package using pip:

```bash
pip install gdrive-core
```

## Setup

Before using `gdrive-core`, ensure you have:

1. **Google Cloud Credentials**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the **Google Drive API** for your project.
   - Download the `credentials.json` file.
   - Place the `credentials.json` file in your working directory.

2. **Token File**:
   - The first time you run the program, it will prompt you to authenticate.
   - A `token.json` file will be created to store access tokens for future use.

## Usage

### 1. Authenticate and Initialize the Client

Initialize the `GDriveCore` client for interacting with Google Drive.

```python
from gdrive_core import GDriveCore

# Initialize the client
client = GDriveCore('credentials.json')
```

### 2. Upload a File with Custom Metadata

Upload a file to Google Drive, optionally adding custom properties.

```python
# Upload a file
file_id = client.upload('example.txt', properties={'is-penguin': 'true', 'category': 'animal'})
print(f"Uploaded file ID: {file_id}")
```

### 3. List Files

List files in the root directory or filter files using queries.

```python
# List all files
files = client.list_files()
print("Files in Drive:")
for f in files:
    print(f"- {f['name']} (ID: {f['id']})")
```

### 4. Download a File

Download a file from Google Drive using its file ID.

```python
# Download a file
download_path = 'downloaded_example.txt'
client.download(file_id, download_path)
print(f"File downloaded to: {download_path}")
```

### 5. Create a Folder

Create a new folder in Google Drive to organize your files.

```python
# Create a folder
folder_id = client.create_folder('NewFolder')
print(f"Folder created with ID: {folder_id}")
```

### 6. Move a File to a Folder

Move an existing file into a specific folder.

```python
# Move the file to the new folder
client.move(file_id, new_parent_id=folder_id)
print("File moved successfully!")
```

### 7. Update File Metadata

Update a file's name or description.

```python
# Update file metadata
client.update_metadata(file_id, new_name='renamed_example.txt', new_description='Updated metadata')
print("File metadata updated!")
```

### 8. Search for Files

Search for files matching specific criteria like name or MIME type.

```python
# Search for files
results = client.search(name_contains='example')
print("Search results:")
for file in results:
    print(f"- {file['name']} (ID: {file['id']})")
```

### 9. Batch Delete Files

Delete multiple files at once by providing their file IDs.

```python
# Batch delete files
client.batch_delete([file_id])
print("Files deleted successfully!")
```

## Full Example

Here is a complete example to authenticate, upload, list, move, download, and delete files:

```python
from gdrive_core import GDriveCore

# Initialize the client
client = GDriveCore('credentials.json')

# Upload a file
file_id = client.upload('example.txt', properties={'is-penguin': 'true'})
print(f"Uploaded file ID: {file_id}")

# Create a folder
folder_id = client.create_folder('NewFolder')
print(f"Created folder ID: {folder_id}")

# Move the file to the folder
client.move(file_id, new_parent_id=folder_id)
print("File moved successfully!")

# List files in the folder
files = client.list_files(query=f"'{folder_id}' in parents")
print("Files in folder:")
for f in files:
    print(f"- {f['name']} (ID: {f['id']})")

# Download the file
download_path = 'downloaded_example.txt'
client.download(file_id, download_path)
print(f"File downloaded to: {download_path}")

# Update file metadata
client.update_metadata(file_id, new_name='renamed_example.txt', new_description='Updated metadata')
print("File metadata updated!")

# Delete the file
client.delete(file_id)
print("File deleted successfully!")
```

## Troubleshooting

- **Missing `credentials.json`**: Ensure the `credentials.json` file is placed in the working directory.
- **Token Issues**: If you face authentication problems, delete the `token.json` file and re-authenticate.
- **Custom Metadata**: Ensure custom property keys and values conform to Google Drive's property limitations.

## License

`gdrive-core` is released under the MIT License.

