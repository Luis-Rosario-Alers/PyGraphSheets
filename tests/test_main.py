import json
import os
import unittest
import unittest.mock as mock
from builtins import isinstance
from dotenv import load_dotenv
import self as self

from PyGraphSheets.main import fetch_data_from_sheets, file_path

load_dotenv("secrets_tests.env")


def test_get_value_from_json(self):
    with mock.patch("PyGraphSheets.main.Credentials") as mock_creds, mock.patch(
        "PyGraphSheets.main.gspread"
    ) as mock_gspread, mock.patch(
        "PyGraphSheets.main.input",
        side_effect=["Sheet1,Sheet2", "label", "directory", "plot.png"],
    ):

        # Arrange
        expected_creds = mock.Mock()
    mock_creds.from_service_account_file.return_value = expected_creds

    # Act
    creds = mock_creds.from_service_account_file(
        file_path, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    self.assertIsNotNone(creds)
    self.assertEqual(creds, expected_creds)

    # Arrange
    expected_client = mock.Mock()
    mock_gspread.authorize.return_value = expected_client

    # Act
    client = mock_gspread.authorize(creds)
    self.assertIsNotNone(client)
    self.assertEqual(client, expected_client)

    # Arrange
    sheet_id = os.getenv("SHEET_ID")
    self.assertIsNotNone(sheet_id, "SHEET_ID environment variable is not set")

    # Act
    mock_sheet = mock.Mock()
    mock_client = mock.Mock()
    mock_client.open_by_key.return_value = mock_sheet
    mock_gspread.authorize.return_value = mock_client

    # Assert
    self.assertIsNotNone(mock_client.open_by_key(sheet_id))

    # Arrange
    mock_worksheet = mock.Mock()
    mock_sheet.worksheet.return_value = mock_worksheet
    mock_worksheet.col_values.side_effect = [["1", "2", "3"], ["4", "5", "6"]]

    # Act
    data = fetch_data_from_sheets(sheet_id, ["Sheet1", "Sheet2"], [1, 3])

    # Assert
    self.assertIn("Sheet1", data)
    self.assertIn("Sheet2", data)
    self.assertEqual(data["Sheet1"], [["1", "2", "3"], ["4", "5", "6"]])
    self.assertEqual(data["Sheet2"], [["1", "2", "3"], ["4", "5", "6"]])
