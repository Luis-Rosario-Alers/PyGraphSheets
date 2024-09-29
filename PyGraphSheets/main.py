import logging
import os
import json
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError
import matplotlib.pyplot as plt

# Read configuration from config.json
with open("config.json") as config_file:
    config = json.load(config_file)
    file_path = config["file_path"]
    sheet_id = config["sheet_id"]
    logs_directory = config["logs_directory"]
    columns = config["columns"]
    plot_settings = config["plot_settings"]
    logging_level = config["logging_level"]

# Ensure the logs directory exists
if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)

# Configure logging to write to a file in the logs directory
log_file_path = os.path.join(logs_directory, "app.log")
logging.basicConfig(
    filename=log_file_path,
    level=getattr(logging, logging_level.upper(), logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

logger.info("Starting the program")

if not file_path or not os.path.exists(file_path):
    raise ValueError("File path is invalid or does not exist.")

if not sheet_id:
    raise ValueError("SHEET_ID is not set in the configuration file.")


def get_value_from_json(file_path):
    try:
        with open(file_path) as f:
            json_data = json.load(f)
            return json_data
    except json.JSONDecodeError as JSONerror:
        logger.error(f"An error occurred while decoding JSON: {JSONerror}")
    except FileNotFoundError as NoFileError:
        logger.error(f"File not found: {NoFileError}")
    except Exception as UnexpectedError:
        logger.error(f"An unexpected error occurred: {UnexpectedError}")
    finally:
        logger.info("Attempted to read JSON file.")


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(file_path, scopes=SCOPES)
client = gspread.authorize(creds)

try:
    client.open_by_key(sheet_id)
except gspread.exceptions.SpreadsheetNotFound:
    raise ValueError("Invalid SHEET_ID. The sheet does not exist.")
else:
    sheet_names = input("Please enter the sheet names separated by commas: ").split(",")
    available_sheets = [ws.title for ws in client.open_by_key(sheet_id).worksheets()]
    if not sheet_names or any(not name.strip() for name in sheet_names):
        raise ValueError("Sheet names cannot be empty.")
    if any(name.strip() not in available_sheets for name in sheet_names):
        raise ValueError(
            "One or more sheet names do not exist in the available sheets."
        )


def fetch_data_from_sheets(sheet_id, sheet_names, columns):
    data = {}
    try:
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


data = fetch_data_from_sheets(sheet_id, sheet_names, columns)
logger.info(data)
label = input("Please enter the label for the plot: ")

for sheet_name, sheet_data in data.items():
    col1plot = list(map(int, filter(None, sheet_data[0][1:])))
    col3plot = list(map(int, filter(None, sheet_data[1][1:])))
    plt.plot(col1plot, col3plot, label=label)

plt.xlabel(plot_settings["xlabel"])
plt.ylabel(plot_settings["ylabel"])
plt.title(plot_settings["title"])
plt.legend(
    loc=plot_settings["legend_loc"],
    fontsize=plot_settings["legend_fontsize"],
    title=plot_settings["legend_title"],
    title_fontsize=plot_settings["legend_title_fontsize"],
    shadow=plot_settings["legend_shadow"],
    frameon=plot_settings["legend_frameon"],
)

directory = input("Please enter the directory path to save the plot: ")
logger.info(f"User entered directory path: {directory}")

if not os.path.exists(directory):
    os.makedirs(directory)
    logger.info(f"Directory created: {directory}")
else:
    logger.info(f"Directory already exists: {directory}")

file_name = input("Please enter the file name to save the plot (e.g., plot.png): ")
logger.info(f"User entered file name: {file_name}")

file_path = os.path.join(directory, file_name)
logger.info(f"Full file path created: {file_path}")

plt.savefig(file_path)
logger.info(f"Plot saved to {file_path}")
print(f"Plot saved to {file_path}")
plt.show()
logger.info("Program completed successfully")