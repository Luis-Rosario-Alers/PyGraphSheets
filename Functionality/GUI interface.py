import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtGui import QIcon
import json
import os
import logging
from google_sheets_fetcher import fetch_data_from_sheets
from data_plotter import plot_data


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Google Sheets Data Plotter")
        self.setGeometry(100, 100, 800, 400)

        # Set the window icon
        icon_path = "icon.ico"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Icon file not found: {icon_path}")

        layout = QVBoxLayout()

        self.config_path = QLineEdit(self)
        self.config_path.setPlaceholderText("Configuration File")
        layout.addWidget(self.config_path)

        self.browse_config_btn = QPushButton("Browse", self)
        self.browse_config_btn.clicked.connect(self.browse_config)
        layout.addWidget(self.browse_config_btn)

        self.sheet_names = QLineEdit(self)
        self.sheet_names.setPlaceholderText("Sheet Names (comma-separated)")
        layout.addWidget(self.sheet_names)

        self.label = QLineEdit(self)
        self.label.setPlaceholderText("Label for Plot")
        layout.addWidget(self.label)

        self.directory = QLineEdit(self)
        self.directory.setPlaceholderText("Directory to Save Plot")
        layout.addWidget(self.directory)

        self.browse_directory_btn = QPushButton("Browse", self)
        self.browse_directory_btn.clicked.connect(self.browse_directory)
        layout.addWidget(self.browse_directory_btn)

        self.file_name = QLineEdit(self)
        self.file_name.setPlaceholderText("File Name for Plot")
        layout.addWidget(self.file_name)

        self.run_btn = QPushButton("Run", self)
        self.run_btn.clicked.connect(self.run)
        layout.addWidget(self.run_btn)

        self.setLayout(layout)

        # Apply styles
        self.setStyleSheet(
            """
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #34495e;
                border: 1px solid #1abc9c;
                padding: 5px;
                border-radius: 3px;
                color: #ecf0f1;
            }
            QPushButton {
                background-color: #1abc9c;
                border: none;
                padding: 10px;
                border-radius: 3px;
                color: #ecf0f1;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
        """
        )

    def browse_config(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Configuration File",
            "",
            "JSON Files (*.json)",
            options=options,
        )
        if file:
            self.config_path.setText(file)

    def browse_directory(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", options=options
        )
        if directory:
            self.directory.setText(directory)

    def run(self):
        try:

            with open(self.config_path.text()) as config_file:
                config = json.load(config_file)
                file_path = config["file_path"]
                sheet_id = config["sheet_id"]
                logs_directory = config["logs_directory"]
                columns = config["columns"]
                plot_settings = config["plot_settings"]
                logging_level = config["logging_level"]

            if not os.path.exists(logs_directory):
                os.makedirs(logs_directory)

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

            sheet_names = self.sheet_names.text().split(",")
            data = fetch_data_from_sheets(file_path, sheet_id, sheet_names, columns)
            logger.info("%s", data)
            if not os.path.exists(self.directory.text()):
                os.makedirs(self.directory.text())
                logger.info(f"Directory created: {self.directory.text()}")
            else:
                logger.info(f"Directory already exists: {self.directory.text()}")

            plot_data(
                data,
                plot_settings,
                self.label.text(),
                self.directory.text(),
                self.file_name.text(),
            )

            logger.info("Program completed successfully")
            QMessageBox.information(self, "Success", "Plot created successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if os.path.exists("icon.ico"):
        app.setWindowIcon(QIcon("icon.ico"))  # Set the taskbar icon
    else:
        print(f"Icon file not found...")
    ex = App()
    ex.show()
    sys.exit(app.exec_())
