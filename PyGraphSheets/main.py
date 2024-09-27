import pandas as pd
import matplotlib as plt
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Authenticate and create a service object
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)

# The ID of your spreadsheet and the range of data you want to retrieve
SPREADSHEET_ID = '1rsQd4WuuAqllnB4vlJTEV5GnC2IuRBG_CQOhcgpA8dk'
RANGE_NAME = 'Sheet1!A1:B10'  # Adjust the range as necessary

# Call the Sheets API to get the data
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

if not values:
    print('No data found.')
else:
    # Convert the data into a DataFrame
    df = pd.DataFrame(values[1:], columns=values[0])  # Use the first row as column headers
    print(df)

    # Plot the data
    df.plot(kind='line', x='Date', y='Value')  # Adjust column names as needed
    plt.title('Sample Data from Google Sheets')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.show()