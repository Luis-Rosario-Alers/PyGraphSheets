import logging
import os
import json
from google_sheets_fetcher import fetch_data_from_sheets
from data_plotter import plot_data

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

# Fetch data from Google Sheets
sheet_names = input(
    "Please enter the sheet names separated by commas: ").split(",")
data = fetch_data_from_sheets(file_path, sheet_id, sheet_names, columns)
logger.info(data)

# Plot data
label = input("Please enter the label for the plot: ")
directory = input("Please enter the directory path to save the plot: ")
logger.info(f"User entered directory path: {directory}")

if not os.path.exists(directory):
    os.makedirs(directory)
    logger.info(f"Directory created: {directory}")
else:
    logger.info(f"Directory already exists: {directory}")

file_name = input(
    "Please enter the file name to save the plot (e.g., plot.png): ")
logger.info(f"User entered file name: {file_name}")

plot_data(data, plot_settings, label, directory, file_name)

logger.info("Program completed successfully")
