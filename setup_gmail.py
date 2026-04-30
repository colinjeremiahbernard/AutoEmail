from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Define scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    # Assumes credentials.json is downloaded from Google Cloud
    if not os.path.exists('credentials.json'):
        print("Please download credentials.json from Google Cloud Console.")
        return

    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Save token
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    print("token.json created successfully!")

if __name__ == '__main__':
    main()