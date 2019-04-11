from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import json

with open('credentials.json') as f:
    creds = json.load(f)

client_id = creds['web']['client_id']
client_secret = creds['web']['client_secret']
token_uri = creds['web']['token_uri']
SCOPES = ['https://www.googleapis.com/auth/documents']


def callback(request_id, response, exception):
    if exception:
        print(exception)
    else:
        print("Permission Id: %s" % response.get('id'))


def create_doc(access_token, content, filename):
    user_creds = Credentials(token=access_token, token_uri=token_uri,
                             client_id=client_id, client_secret=client_secret)
    service = build('docs', 'v1', credentials=user_creds)

    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': content
            }
        }
    ]

    doc = service.documents().create(body={'title': filename}).execute()
    document_id = doc['documentId']
    service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    return document_id


def get_docs(access_token):
    user_creds = Credentials(token=access_token, token_uri=token_uri,
                             client_id=client_id, client_secret=client_secret)
    service = build('drive', 'v3', credentials=user_creds)

    drive_files = service.files().list().execute()
    return drive_files


def share_doc(access_token, emails, permission, id):
    user_creds = Credentials(token=access_token, token_uri=token_uri,
                             client_id=client_id, client_secret=client_secret)
    service = build('drive', 'v3', credentials=user_creds)
    batch = service.new_batch_http_request(callback=callback)

    for email in emails:
        user_permission = {
            'type': 'user',
            'role': permission,
            'emailAddress': email
        }
        batch.add(service.permissions().create(
            fileId=id,
            body=user_permission,
            fields='id'
        ))
    batch.execute()
