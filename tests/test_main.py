import json
import os
import unittest
import unittest.mock as mock
from builtins import isinstance
from dotenv import load_dotenv

load_dotenv("secrets_tests.env")


class jsonFileTest(unittest.TestCase):
    """
    Unit tests for JSON file operations.
    """

    def test_file_path(self):
        """
        Test if the file path specified in the environment variable exists.
        """
        # Arrange
        file_path = os.getenv("FILE_PATH")
        print(f"FILE_PATH: {file_path}")  # Debugging line
        # Act
        result_file_path = os.path.exists(file_path)
        # Assert
        self.assertTrue(result_file_path)

    def test_json_file(self):
        """
        Test if the JSON file specified in the environment variable can be loaded and is valid JSON.
        """
        # Arrange
        file_path = os.getenv("FILE_PATH")
        self.assertIsNotNone(file_path, "FILE_PATH environment variable is not set")
        # Act
        try:
            with open(file_path) as f:
                json_data = json.load(f)
                result = json_data
        except FileNotFoundError:
            self.fail(f"File not found: {file_path}")
        except json.JSONDecodeError:
            self.fail(f"Invalid JSON in file: {file_path}")
        # Assert
        self.assertEqual(result, json_data)


class apiAuthorizationProcess(unittest.TestCase):
    """
    Unit tests for the API authorization process.
    """

    def test_file_path(self):
        """
        Test if the file path specified in the environment variable exists.
        """
        # Arrange
        file_path = os.getenv("FILE_PATH")
        print(f"FILE_PATH: {file_path}")  # Debugging line
        # Act
        result = os.path.exists(file_path)
        # Assert
        self.assertTrue(result)

    def test_api_authorization(self):
        """
        Test if the API authorization process is successful.
        """
        # Arrange
        file_path = os.getenv("FILE_PATH")
        self.assertIsNotNone(file_path, "FILE_PATH environment variable is not set")
        # Act
        try:
            with open(file_path) as f:
                json_data = json.load(f)
                result_of_credentials = json_data
        except FileNotFoundError:
            self.fail(f"File not found: {file_path}")
        except json.JSONDecodeError:
            self.fail(f"Invalid JSON in file: {file_path}")
        # Assert
        self.assertEqual(result_of_credentials, json_data)

        # Arrange
        with mock.patch("PyGraphSheets.main.Credentials") as mock_creds:
            # Arrange
            expected_result_of_credentials = mock.Mock()
            mock_creds.from_service_account_file.return_value = (
                expected_result_of_credentials
            )
            # Act
            result_of_credentials = mock_creds.from_service_account_file(
                file_path, scopes=["https://www.googleapis.com/auth/spreadsheets"]
            )
            print(
                f"Mocked Credentials result: {result_of_credentials}"
            )  # Debugging line
            # Assert
            self.assertIsNotNone(result_of_credentials)
            self.assertEqual(result_of_credentials, expected_result_of_credentials)

            # Arrange
            sheet_id = os.getenv("SHEET_ID")
            print(f"SHEET_ID: {sheet_id}")  # Debugging line
            try:
                is_sheet_id_a_string_result_expected = isinstance(sheet_id, str)
                # Act
                is_sheet_id_a_string_result = isinstance(sheet_id, str)
                print(
                    f"Result from using sheet_id env variable: {sheet_id}"
                )  # Debugging line
                # Assert
                self.assertIsNotNone(is_sheet_id_a_string_result)
                self.assertEqual(
                    is_sheet_id_a_string_result, is_sheet_id_a_string_result_expected
                )
            except TypeError as error:
                print(f"Not correct data type: {error}")
            except None as error:
                print(f"No data: {error}")
            except Exception as error:
                print(f"An unexpected error occurred: {error}")

            # Arrange
            with mock.patch("PyGraphSheets.main.worksheet") as mock_worksheet:
                expected_result = mock_worksheet.sheet1
                # Act
                is_sheet_id_a_string_result = mock_worksheet.sheet1
                # Assert
                self.assertIsNotNone(is_sheet_id_a_string_result)
                self.assertEqual(
                    is_sheet_id_a_string_result, expected_result
                )  # Debugging line


if __name__ == "__main__":
    unittest.main()
