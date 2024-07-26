from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'homework.json'
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets']
)
google_sheet_id_users = '1VWNoXdFodHUC51o0ajNwWq2Wi-Sw2Ib_qP0qZVV40VA'
service = build('sheets', 'v4', credentials=creds)
