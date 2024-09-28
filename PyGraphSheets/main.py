from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
import matplotlib.pyplot as plt
import gspread
import os
import json
from dotenv import load_dotenv

# Load environment variables from env file
load_dotenv('secrets.env')

print(os.getenv("SHEET_ID"))
# Get the file path from the environment variable

sheet_id = os.getenv("SHEET_ID")
file_path = os.getenv("FILE_PATH")
if not file_path:
    raise ValueError("FILE_PATH environment variable is not set or is empty.")
elif not os.path.exists(file_path):
    raise FileNotFoundError(f"File path {file_path} does not exist.")


def get_value_from_json(file_path):
    """
    Reads a JSON file and returns its content.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The content of the JSON file.
    """
    try:
        with open(file_path) as f:
            json_data = json.load(f)
            return json_data
    except json.JSONDecodeError as error:
        print(f"An error occurred while decoding JSON: {error}")
    except FileNotFoundError as error:
        print(f"File not found: {error}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")
    finally:
        print('Attempted to read JSON file.')


# Define the scope for accessing Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Get credentials from the service account file and authorize with those credentials
creds = Credentials.from_service_account_file(file_path, scopes=SCOPES)
client = gspread.authorize(creds)


# Specify the Google Sheet by its ID
worksheet = client.open_by_key(sheet_id)

# Fetch data values from the necessary columns
try:
    columns = [1, 3, 6, 7, 8, 9, 11]
    data = [worksheet.sheet1.col_values(col) for col in columns]
    print(data)
except HttpError as error:
    print(f"An error occurred with the Google Sheets API: {error}")
except gspread.exceptions.SpreadsheetNotFound as error:
    print(f"Spreadsheet not found: {error}")
except Exception as error:
    print(f"An unexpected error occurred: {error}")

# Convert column values to integers, ignoring empty values
col1plot = list(map(int, filter(None, data[0][1:])))
print(col1plot)
col3plot = list(map(int, filter(None, data[1][1:])))
print(col3plot)

# Plot the data
plt.plot(col1plot, col3plot, label='Before Caffeine vs. After Caffeine')
plt.xlabel('Before Caffeine')
plt.ylabel('After Caffeine')
plt.title('Before Caffeine vs. After Caffeine')
plt.legend(loc='upper left', fontsize='medium', title='Legend', title_fontsize='large', shadow=True, frameon=True)
plt.show()
