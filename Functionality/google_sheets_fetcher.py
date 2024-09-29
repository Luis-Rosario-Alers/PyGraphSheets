# google_sheets_fetcher.py

import logging

import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)


def fetch_data_from_sheets(file_path, sheet_id, sheet_names, columns):
    """
    Fetch data from Google Sheets.

    Args:
        file_path (str): Path to the service account file.
        sheet_id (str): ID of the Google Sheet.
        sheet_names (list): List of sheet names to fetch data from.
        columns (list): List of column indices to fetch data from.

    Returns:
        dict: Dictionary containing the fetched data.
    """
    data = {}
    try:
        creds = Credentials.from_service_account_file(
            file_path, scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id)
        available_sheets = sheet.worksheets()
        available_sheet_names = [ws.title for ws in available_sheets]
        logger.info(f"Available sheets: {available_sheet_names}")

        for sheet_name in sheet_names:
            sheet_name = sheet_name.strip()
            if sheet_name not in available_sheet_names:
                logger.error(f"Worksheet '{sheet_name}' not found in available sheets.")
                continue

            worksheet = sheet.worksheet(sheet_name)
            sheet_data = [worksheet.col_values(col) for col in columns]
            data[sheet_name] = sheet_data
    except HttpError as error:
        logger.error(f"An error occurred with the Google Sheets API: {error}")
    except gspread.exceptions.WorksheetNotFound as error:
        logger.error(f"Worksheet '{sheet_name}' not found: {error}")
    except Exception as error:
        logger.error(f"An unexpected error occurred: {error}")
    return data
