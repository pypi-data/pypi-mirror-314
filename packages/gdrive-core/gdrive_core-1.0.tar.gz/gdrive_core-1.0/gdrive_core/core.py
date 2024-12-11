import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']

class GDriveCore:
    """Google Drive API Client for easy file and folder management."""

    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        """Initialize and authenticate the Google Drive client."""
        self.service = self._authenticate(credentials_file, token_file)

    def _authenticate(self, credentials_file, token_file):
        """Authenticate and return the Google Drive service."""
        creds = None
        if os.path.exists(token_file):
            try:
                creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            except ValueError:
                os.remove(token_file)
                creds = None
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        return build('drive', 'v3', credentials=creds)

    def upload(self, file_path, parent_id=None, properties=None):
        """Upload a file to Google Drive with optional custom properties."""
        file_name = os.path.basename(file_path)
        metadata = {'name': file_name}
        if parent_id:
            metadata['parents'] = [parent_id]
        if properties:
            metadata['properties'] = properties

        media = MediaFileUpload(file_path, resumable=True)
        file = self.service.files().create(body=metadata, media_body=media, fields='id').execute()
        return file.get('id')

    def list_files(self, query=None):
        """List files in Google Drive based on a query."""
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        return results.get('files', [])

    def download(self, file_id, local_path):
        """Download a file from Google Drive."""
        request = self.service.files().get_media(fileId=file_id)
        with open(local_path, 'wb') as f:
            f.write(request.execute())

    def delete(self, file_id):
        """Delete a file from Google Drive."""
        self.service.files().delete(fileId=file_id).execute()

    def create_folder(self, folder_name, parent_id=None):
        """Create a new folder in Google Drive."""
        metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
        if parent_id:
            metadata['parents'] = [parent_id]
        folder = self.service.files().create(body=metadata, fields='id').execute()
        return folder.get('id')

    def move(self, file_id, new_parent_id, old_parent_id=None):
        """Move a file to a new folder."""
        file = self.service.files().update(
            fileId=file_id,
            addParents=new_parent_id,
            removeParents=old_parent_id,
            fields='id, parents'
        ).execute()
        return file

    def update_metadata(self, file_id, new_name=None, new_description=None):
        """Update file metadata."""
        metadata = {}
        if new_name:
            metadata['name'] = new_name
        if new_description:
            metadata['description'] = new_description
        updated_file = self.service.files().update(
            fileId=file_id,
            body=metadata,
            fields='id, name, description'
        ).execute()
        return updated_file

    def search(self, name_contains=None, mime_type=None):
        """Search for files in Google Drive."""
        query = []
        if name_contains:
            query.append(f"name contains '{name_contains}'")
        if mime_type:
            query.append(f"mimeType='{mime_type}'")
        query = " and ".join(query)
        return self.list_files(query=query)

    def batch_delete(self, file_ids):
        """Delete multiple files from Google Drive."""
        for file_id in file_ids:
            self.delete(file_id)