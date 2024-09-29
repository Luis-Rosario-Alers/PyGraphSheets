from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
import matplotlib.pyplot as plt
import gspread
import os
import json
from gspread import worksheet
while True:
    try:
        file_path = input("Please enter the file path of your JSON credentials: ")
        if not file_path or not os.path.exists(file_path):
            raise ValueError("File path is invalid or does not exist.")
        break  # Exit the loop if the file path is valid
    except ValueError as e:
        print(f"Invalid input: {e}. Please enter a valid value.")


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
    except json.JSONDecodeError as JSONerror:
        print(f"An error occurred while decoding JSON: {JSONerror}")
    except FileNotFoundError as NoFileError:
        print(f"File not found: {NoFileError}")
    except Exception as UnexpectedError:
        print(f"An unexpected error occurred: {UnexpectedError}")
    finally:
        print("Attempted to read JSON file.")

# Define the scope for accessing Google Sheets API
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Get credentials from the service account file and authorize with those credentials
creds = Credentials.from_service_account_file(file_path, scopes=SCOPES)
client = gspread.authorize(creds)


while True:
    try:
        sheet_id = input("Please enter the SHEET_ID: ")
        try:
            client.open_by_key(sheet_id)
        except gspread.exceptions.SpreadsheetNotFound:
            raise ValueError("Invalid SHEET_ID. The sheet does not exist.")
    except ValueError as e:
        print(f"Invalid input: {e}. Please enter a valid value.")
        continue
    else:
        sheet_names = input("Please enter the sheet names separated by commas: ").split(',')
        available_sheets = [ws.title for ws in client.open_by_key(sheet_id).worksheets()]
        if not sheet_names or any(not name.strip() for name in sheet_names):
            raise ValueError("Sheet names cannot be empty.")
        if any(name.strip() not in available_sheets for name in sheet_names):
            raise ValueError("One or more sheet names do not exist in the available sheets.")
        else:
            break

if not file_path:
    raise ValueError("File cannot be empty.")
elif not os.path.exists(file_path):
    raise FileNotFoundError(f"File path {file_path} does not exist.")


def fetch_data_from_sheets(sheet_id, sheet_names, columns):
    data = {}
    try:
        # Fetch all sheet names in the document
        sheet = client.open_by_key(sheet_id)
        available_sheets = sheet.worksheets()
        available_sheet_names = [ws.title for ws in available_sheets]
        print(f"Available sheets: {available_sheet_names}")

        for sheet_name in sheet_names:
            sheet_name = sheet_name.strip()
            if sheet_name not in available_sheet_names:
                print(f"Worksheet '{sheet_name}' not found in available sheets.")
                continue

            worksheet = sheet.worksheet(sheet_name)
            sheet_data = [worksheet.col_values(col) for col in columns]
            data[sheet_name] = sheet_data
    except HttpError as error:
        print(f"An error occurred with the Google Sheets API: {error}")
    except gspread.exceptions.WorksheetNotFound as error:
        print(f"Worksheet '{sheet_name}' not found: {error}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")
    return data


columns = [1, 3, 6, 7, 8, 9, 11]
data = fetch_data_from_sheets(sheet_id, sheet_names, columns)
print(data)
label = input('Please enter the label for the plot: ')


for sheet_name, sheet_data in data.items():
    col1plot = list(map(int, filter(None, sheet_data[0][1:])))
    col3plot = list(map(int, filter(None, sheet_data[1][1:])))
    plt.plot(col1plot, col3plot, label=label)


while True:
    try:
        xlabel = input("Please enter the x-axis label: ")
        ylabel = input("Please enter the y-axis label: ")
        title = input("Please enter the title of the plot: ")
        legend_loc = input("Please enter the legend location (e.g., 'upper left'): ")
        legend_fontsize = input("Please enter the legend font size (e.g., 'medium'): ")
        legend_title = input("Please enter the legend title: ")
        legend_title_fontsize = input("Please enter the legend title font size (e.g., 'large'): ")
        legend_shadow = input("Should the legend have a shadow? (True/False): ").lower() == 'true'
        legend_frameon = input("Should the legend have a frame? (True/False): ").lower() == 'true'
    except ValueError as e:
        print(f"Invalid input: {e}. Please enter a valid value.")
        continue
    else:
        break


plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.legend(
    loc=legend_loc,
    fontsize=legend_fontsize,
    title=legend_title,
    title_fontsize=legend_title_fontsize,
    shadow=legend_shadow,
    frameon=legend_frameon,
)
plt.show()

