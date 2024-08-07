from concurrent.futures import TimeoutError
from datetime import datetime
import json
from google.cloud import pubsub_v1
import os
from django.utils import timezone
import requests
import tabula
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email_invoice_retriever import retrieve_pdf_invoice
from groceries.utils.preprocessing import scan_prices

project_id = "domfin-429717"
subscription_id = "new_colruyt_invoice"
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.]
# 
API_PATH = '/api/v1/groceries'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
print("-"*50)
print(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())



service = build('gmail', 'v1', credentials=creds)
request = {
  'labelIds': ['INBOX'],
  'labelFilterAction': 'include',
  'topicName': 'projects/domfin-429717/topics/domfin'
}
service.users().watch(userId='me', body=request).execute()

subscriber = pubsub_v1.SubscriberClient()
# final form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    print(f"from {message.data}")
    print(f"Message data: {message.data.decode('utf-8')}")
    if retrieve_pdf_invoice():
        dfs = tabula.read_pdf(str(datetime.now().strftime('%Y-%m-%d')) + '_colryt_invoice.pdf', pages='all')
        df = scan_prices(dfs).rename(columns={'article': 'shop_id', 'total_spent': 'cost'})        # TODO: call the endpoint with the data
        json_data = {

            "date": timezone.now(), #datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "+00:00",
            "lines": df.to_dict(orient='records')
        }
        
        json_str = json.dumps(json_data, indent=4)
        print(json_str)
        
        # Send JSON to endpoint
        endpoint_url = "http://dfa-django:8000" + API_PATH + "/analytics/invoice/"
        response = requests.post(endpoint_url, json=json_data, verify=False)
        print(f"Response from endpoint: {response.status_code} - {response.text}")

        print(df)
        #print(df.total_spent.sum())
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.

