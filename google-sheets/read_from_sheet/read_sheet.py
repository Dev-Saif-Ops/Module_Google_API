import os
import sys
import git
repo_path = str(git.Repo('.', search_parent_directories=True).working_tree_dir)
sys.path.append(repo_path)
os.chdir(repo_path)

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from credentials.credential_manager import credential_management
import json
import pandas as pd
# Read the ID and range of a sample spreadsheet from config.json
config_json = open("google-sheets/read-from-sheet/read_from_sheet_config.json")
config_data = json.load(config_json)
SAMPLE_SPREADSHEET_ID = config_data["READ_SPREADSHEET_ID"]
SAMPLE_RANGE_NAME = config_data["READ_RANGE"]
DATA_WORKING_DIR = str("google-sheets/read-from-sheet/") + str(config_data["DATA_WORKING_DIR"])


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = credential_management()

    try:

        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])
        if not values:
            print("No data found.")
            return

        df = pd.DataFrame(values)
        df.to_csv(str(DATA_WORKING_DIR)+"/"+str("out.csv"), index=False, header=False)

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
