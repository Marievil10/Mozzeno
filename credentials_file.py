import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_credentials(doc_name, sheet):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    document_name = doc_name
    sheet_name = client.open(document_name).worksheet(sheet)
    return sheet_name
