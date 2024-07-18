from datetime import datetime, timedelta
import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def retrieve_pdf_invoice():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, raise 
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      raise Exception("Please provide the credentials.json file")
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    # Calculate time 2 minutes ago
    time_2_minutes_ago = int((datetime.now() - timedelta(minutes=1)).timestamp())
    query = f"from:(alexllobet369@gmail.com OR mricomorillo@gmail.com) after:{time_2_minutes_ago}"
    
    results = service.users().messages().list(userId="me", q=query).execute()
    messages = results.get("messages", [])
    message_count = 0
    pdf_was_found = False
    for message in messages:
        msg = service.users().messages().get(userId="me", id=message["id"]).execute()
        message_count = message_count + 1
        email_data = msg["payload"]["headers"]
        for values in email_data:
            name = values["name"]
            if name == "From":
                from_name = values["value"]
                print(from_name)
                subject = [j["value"] for j in email_data if j["name"] == "Subject"]
                print(subject)

        if "parts" in msg["payload"]:
                for part in msg["payload"]["parts"]:
                    if part["mimeType"] in ["text/plain", "text/html"]:
                        data = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                        print("Message body:", data)
                    
                    # Retrieve attachments
                    if part["filename"]:
                        attachment_id = part["body"]["attachmentId"]
                        attachment = service.users().messages().attachments().get(userId="me", messageId=message["id"], id=attachment_id).execute()
                        file_data = base64.urlsafe_b64decode(attachment["data"])
                        path = str(datetime.now().strftime('%Y-%m-%d')) + '_colryt_invoice.pdf'
                        with open(path, "wb") as f:
                            f.write(file_data)
                        print(f"Attachment {part['filename']} saved.")
                        pdf_was_found = True
    if not pdf_was_found:
       print("Emails were found but no PDF attachments were found.")
    return pdf_was_found
        

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")

