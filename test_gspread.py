import gspread
import toml
import os

def test_connection():
    try:
        secrets = toml.load(r"d:\CUB_LOG\.streamlit\secrets.toml")
        credentials = secrets["connections"]["gsheets"]
        print("Loaded secrets!")
    except Exception as e:
        print("Failed to load secrets:", e)
        return

    try:
        gc = gspread.service_account_from_dict(credentials)
        print("Successfully authenticated with Service Account:", credentials.get("client_email"))
    except Exception as e:
        print("Failed to authenticate:", e)
        return

    LOG_SHEET_URL = "https://docs.google.com/spreadsheets/d/17ygWdYJSKHKLrx5_8iMBuSkTaWuC_i1X47ljcKdRo98/edit?gid=1732522338#gid=1732522338"
    
    try:
        sh = gc.open_by_url(LOG_SHEET_URL)
        print("Successfully opened sheet:", sh.title)
        
        # Test worksheets
        print("Worksheets:", [w.title for w in sh.worksheets()])
    except Exception as e:
        print("Failed to open sheet via URL:", e)
        print("Did you share the Google Sheet with", credentials.get("client_email"), "?")

if __name__ == "__main__":
    test_connection()
