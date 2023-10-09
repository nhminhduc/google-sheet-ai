import pandas as pd

SHEET_ID = "1eJC_UnEH2xDzPqwuJP1X7KxOTgo0fMKu0oslUn9EDaU"
SHEET_NAME = "Sheet1"


def fetch_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    df = pd.read_csv(url)
    data_dict = df.to_dict(orient="records")
    return data_dict
