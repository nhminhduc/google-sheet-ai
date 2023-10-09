import gspread
from google.oauth2.service_account import Credentials

# Define the scope
SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]


def access_google_sheet():
    # Load credentials from file
    try:
        creds = Credentials.from_service_account_file(
            "service_account.json", scopes=SCOPES
        )
        client = gspread.authorize(creds)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

    # Access the Google Sheet
    try:
        sheet = client.open_by_key(
            "1eJC_UnEH2xDzPqwuJP1X7KxOTgo0fMKu0oslUn9EDaU"
        ).sheet1
        data = sheet.get_all_records()
        return data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
