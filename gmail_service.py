"""
Provides a service interface to interact with the Gmail API.
"""

import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def get_gmail_service():
    """
    Initializes and returns an authenticated Gmail API service instance.

    Returns:
        The authenticated Gmail API service instance.
    """
    creds = Credentials.from_authorized_user_file('token.json')
    return build('gmail', 'v1', credentials=creds)

def get_unread_emails(service):
    """
    Retrieves a list of unread email messages from the user's inbox.

    Args:
        service: The authenticated Gmail API service instance.

    Returns:
        list: A list of message dictionaries.
    """
    results = service.users().messages().list(userId='me', labelIds=['UNREAD']).execute()
    messages = results.get('messages', [])
    return messages

def get_email_content(service, msg_id):
    """
    Fetches the plain text body of a specific email message.

    Args:
        service: The authenticated Gmail API service instance.
        msg_id (str): The ID of the message to retrieve.

    Returns:
        str: The plain text content of the email, or an empty string.
    """
    msg = service.users().messages().get(userId='me', id=msg_id).execute()
    payload = msg['payload']
    parts = payload.get('parts', [])

    for part in parts:
        if part['mimeType'] == 'text/plain':
            data = part['body']['data']
            text = base64.urlsafe_b64decode(data).decode('utf-8', errors='replace')
            return text
    return ""
