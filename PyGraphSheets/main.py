from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
import matplotlib.pyplot as plt
import gspread
import os
import json
from dotenv import load_dotenv

# Load environment variables from 'secrets.env' file
load_dotenv('secrets.env')

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
    with open(file_path) as f:
        return json.load(f)

# Define the scope for accessing Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Get credentials from the service account file and authorize with those credentials
creds = Credentials.from_service_account_file(file_path, scopes=SCOPES)
client = gspread.authorize(creds)

print(client)

# Specify the Google Sheet by its ID
sheet_id = sheet_id
worksheet = client.open_by_key(sheet_id)

# Fetch data values from the necessary columns
try:
    col1 = worksheet.sheet1.col_values(1)
    col3 = worksheet.sheet1.col_values(3)
    col6 = worksheet.sheet1.col_values(6)
    col7 = worksheet.sheet1.col_values(7)
    col8 = worksheet.sheet1.col_values(8)
    col9 = worksheet.sheet1.col_values(9)
    col11 = worksheet.sheet1.col_values(11)
    data = (col1, col3, col6, col7, col8, col9, col11)
    print(data)
 except HttpError as error:
    print(f"An error occurred: {error}")
# Convert column values to integers, ignoring empty values
co1 = list(map(int, filter(None, col1[1:])))
co3 = list(map(int, filter(None, col3[1:])))

# Plot the data
plt.plot(co1, co3, label='Before Caffeine vs. After Caffeine')
plt.xlabel('Before Caffeine')
plt.ylabel('After Caffeine')
plt.title('Before Caffeine vs. After Caffeine')
plt.legend(loc='upper left', fontsize='medium', title='Legend', title_fontsize='large', shadow=True, frameon=True)
plt.show()
