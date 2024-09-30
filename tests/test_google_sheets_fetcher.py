# tests/test_google_sheets_fetcher.py
import unittest
from unittest.mock import patch, MagicMock
from Functionality.google_sheets_fetcher import fetch_data_from_sheets
from googleapiclient.errors import HttpError
import gspread


class TestFetchDataFromSheets(unittest.TestCase):

    @patch('Functionality.google_sheets_fetcher.gspread.authorize')
    @patch('Functionality.google_sheets_fetcher.Credentials.from_service_account_file')
    def test_successful_data_fetch(self, mock_creds, mock_authorize):
        mock_client = MagicMock()
        mock_sheet = MagicMock()
        mock_worksheet = MagicMock()
        mock_worksheet.col_values.side_effect = [['A1', 'A2'], ['B1', 'B2']]
        mock_sheet.worksheet.return_value = mock_worksheet
        mock_client.open_by_key.return_value = mock_sheet
        mock_authorize.return_value = mock_client
        expected = {'Sheet1': [['A1', 'A2'], ['B1', 'B2']]}
        result = fetch_data_from_sheets('file_', 'mock_sheet', ['Sheet1'], [1, 2])
        print(result)
        print(expected)
        self.assertEqual(result, expected)

    @patch('Functionality.google_sheets_fetcher.gspread.authorize')
    @patch('Functionality.google_sheets_fetcher.Credentials.from_service_account_file')
    def test_non_existent_worksheet(self, mock_creds, mock_authorize):
        mock_client = MagicMock()
        mock_sheet = MagicMock()
        mock_client.open_by_key.return_value = mock_sheet
        mock_authorize.return_value = mock_client
        mock_sheet.worksheets.return_value = []

        result = fetch_data_from_sheets('fake_path', 'fake_id', ['NonExistentSheet'], [1, 2])
        self.assertEqual(result, {})

    @patch('Functionality.google_sheets_fetcher.gspread.authorize')
    @patch('Functionality.google_sheets_fetcher.Credentials.from_service_account_file')
    def test_http_error(self, mock_creds, mock_authorize):
        mock_client = MagicMock()
        mock_authorize.side_effect = HttpError(resp=None, content=b'Error')

        result = fetch_data_from_sheets('fake_path', 'fake_id', ['Sheet1'], [1, 2])
        self.assertEqual(result, {})

    @patch('Functionality.google_sheets_fetcher.gspread.authorize')
    @patch('Functionality.google_sheets_fetcher.Credentials.from_service_account_file')
    def test_unexpected_error(self, mock_creds, mock_authorize):
        mock_client = MagicMock()
        mock_authorize.side_effect = Exception('Unexpected error')

        result = fetch_data_from_sheets('fake_path', 'fake_id', ['Sheet1'], [1, 2])
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()