import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QComboBox,
    QCheckBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt
import json
import os
import logging
from google_sheets_fetcher import fetch_data_from_sheets
from data_plotter import plot_data
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_settings()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)

    def initUI(self):
        self.setWindowTitle("Google Sheets Data Plotter")
        self.setGeometry(100, 100, 800, 600)




        layout = QVBoxLayout()

        self.x_columns = QLineEdit(self)
        self.x_columns.setPlaceholderText("X Column Indices (comma-separated)")
        layout.addWidget(self.x_columns)

        self.y_columns = QLineEdit(self)
        self.y_columns.setPlaceholderText("Y Column Indices (comma-separated)")
        layout.addWidget(self.y_columns)

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

        self.graph_type = QComboBox(self)
        self.graph_type.addItems(["Line", "Bar", "Scatter"])
        layout.addWidget(self.graph_type)

        self.export_format = QComboBox(self)
        self.export_format.addItems(["PNG", "PDF", "SVG"])
        layout.addWidget(self.export_format)

        self.real_time_checkbox = QCheckBox("Enable Real-Time Updates", self)
        layout.addWidget(self.real_time_checkbox)

        self.interval_input = QLineEdit(self)
        self.interval_input.setPlaceholderText("Update Interval (seconds)")
        layout.addWidget(self.interval_input)

        self.run_btn = QPushButton("Run", self)
        self.run_btn.clicked.connect(self.run)
        layout.addWidget(self.run_btn)

        self.export_btn = QPushButton("Export", self)
        self.export_btn.clicked.connect(self.export_plot)
        layout.addWidget(self.export_btn)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.canvas)

        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)

        self.setLayout(layout)

        # Connect the checkbox state change signal
        self.real_time_checkbox.stateChanged.connect(self.toggle_real_time_updates)

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

    def load_settings(self):
        settings_path = "settings.json"
        if os.path.exists(settings_path):
            with open(settings_path, "r") as settings_file:
                settings = json.load(settings_file)
                self.config_path.setText(settings.get("last_config_path", ""))
                self.directory.setText(settings.get("last_save_directory", ""))

    def save_settings(self):
        settings = {
            "last_config_path": self.config_path.text(),
            "last_save_directory": self.directory.text()
        }
        with open("settings.json", "w") as settings_file:
            json.dump(settings, settings_file)

    def closeEvent(self, event):
        self.save_settings()
        event.accept()

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
            self.save_settings()  # Save settings immediately after selection

    def browse_directory(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", options=options
        )
        if directory:
            self.directory.setText(directory)
            self.save_settings()  # Save settings immediately after selection

    def run(self):
        try:
            with open(self.config_path.text()) as config_file:
                config = json.load(config_file)
                self.file_path = config["file_path"]
                self.sheet_id = config["sheet_id"]
                self.logs_directory = config["logs_directory"]
                self.columns = config["columns"]
                self.plot_settings = config["plot_settings"]
                self.logging_level = config["logging_level"]

            if not os.path.exists(self.logs_directory):
                os.makedirs(self.logs_directory)

            log_file_path = os.path.join(self.logs_directory, "app.log")
            logging.basicConfig(
                filename=log_file_path,
                level=getattr(logging, self.logging_level.upper(), logging.INFO),
                format="%(asctime)s - %(levelname)s - %(message)s",
            )
            self.logger = logging.getLogger(__name__)

            self.logger.info("Starting the program")

            if not self.file_path or not os.path.exists(self.file_path):
                raise ValueError("File path is invalid or does not exist.")

            if not self.sheet_id:
                raise ValueError("SHEET_ID is not set in the configuration file.")

            if not os.path.exists(self.directory.text()):
                os.makedirs(self.directory.text())
                self.logger.info(f"Directory created: {self.directory.text()}")
            else:
                self.logger.info(f"Directory already exists: {self.directory.text()}")

            self.x_col_indices = list(map(int, self.x_columns.text().split(',')))
            self.y_col_indices = list(map(int, self.y_columns.text().split(',')))

            self.update_plot()  # Initial plot

            if self.real_time_checkbox.isChecked():
                interval = int(self.interval_input.text()) * 1000  # Convert to milliseconds
                self.timer.start(interval)

            self.logger.info("Program completed successfully")
            QMessageBox.information(self, "Success", "Plot created successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_plot(self):
        try:
            sheet_names = self.sheet_names.text().split(",")
            data = fetch_data_from_sheets(self.file_path, self.sheet_id, sheet_names, self.columns)
            self.logger.info(f"Fetched data: {data}")

            self.canvas.axes.clear()  # Clear the axes to refresh the plot
            graph_type = self.graph_type.currentText()
            plot_result = plot_data(data, self.plot_settings, self.label.text(), self.directory.text(),
                                    self.file_name.text(), self.canvas.axes, graph_type, self.x_col_indices,
                                    self.y_col_indices)
            self.canvas.draw()  # Redraw the canvas to reflect the changes
        except Exception as e:
            self.logger.error(f"Error updating plot: {str(e)}")
            QMessageBox.critical(self, "Error", str(e))

    def export_plot(self):
        try:
            export_format = self.export_format.currentText().lower()
            file_path = os.path.join(self.directory.text(), f"{self.file_name.text()}.{export_format}")
            self.canvas.figure.savefig(file_path, format=export_format)
            QMessageBox.information(self, "Success", f"Plot exported as {export_format.upper()} successfully!")
        except Exception as e:
            self.logger.error(f"Error exporting plot: {str(e)}")
            QMessageBox.critical(self, "Error", str(e))

    def toggle_real_time_updates(self, state):
        if state == Qt.Checked:
            interval = int(self.interval_input.text()) * 1000  # Convert to milliseconds
            self.timer.start(interval)
        else:
            self.timer.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if os.path.exists("icon.ico"):
        app.setWindowIcon(QIcon("icon.ico"))  # Set the taskbar icon
    else:
        print("Icon file not found...")
    ex = App()
    ex.show()
    sys.exit(app.exec_())