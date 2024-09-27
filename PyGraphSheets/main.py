from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
import matplotlib
import gspread

# This code is made to have access to the Google spreadsheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# This gets your credentials from service account and authorizes with those credentials
creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
client = gspread.authorize(creds)
# I specify my sheet using by inputting my sheet id so that the program knows specifically which sheet I am accessing.
sheet_id = '1rsQd4WuuAqllnB4vlJTEV5GnC2IuRBG_CQOhcgpA8dk'
worksheet = client.open_by_key(sheet_id)

# This fetches data values from the necessary columns and this step is necessary for verification that the necessary values have been fetched.
values_List = worksheet.sheet1.col_values(1), worksheet.sheet1.col_values(3), worksheet.sheet1.col_values(6), worksheet.sheet1.col_values(7), worksheet.sheet1.col_values(8), worksheet.sheet1.col_values(9), worksheet.sheet1.col_values(11)
data = values_List
print(data)
