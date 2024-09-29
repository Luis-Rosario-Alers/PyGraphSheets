# data_plotter.py

import logging
import os

import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def plot_data(data, plot_settings, label, directory, file_name):
    """Plot data and save the plot to a file.

    :param data: Dictionary containing the data to plot.
    :type data: dict
    :param plot_settings: Dictionary containing plot settings.
    :type plot_settings: dict
    :param label: Label for the plot.
    :type label: str
    :param directory: Directory to save the plot.
    :type directory: str
    :param file_name: File name to save the plot.
    :type file_name: str

    """
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

    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Directory created: {directory}")
    else:
        logger.info(f"Directory already exists: {directory}")

    file_path = os.path.join(directory, file_name)
    plt.savefig(file_path)
    logger.info(f"Plot saved to {file_path}")
    print(f"Plot saved to {file_path}")
    plt.show()
