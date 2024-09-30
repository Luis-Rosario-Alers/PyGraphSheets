# tests/test_data_plotter.py
import sys
import os
import unittest.mock
from Functionality.data_plotter import plot_data


def test_save_plot(tmp_path):
    data = {"sheet1": [[1, 2, 3, 4, 5], [5, 4, 3, 2, 1]]}
    plot_settings = {
        "xlabel": "X Axis",
        "ylabel": "Y Axis",
        "title": "Test Plot",
        "legend_loc": "upper right",
        "legend_fontsize": 10,
        "legend_title": "Legend",
        "legend_title_fontsize": 12,
        "legend_shadow": True,
        "legend_frameon": True,
    }
    file_path = tmp_path / "test_plot.png"
    plot_data(data, plot_settings, "Test Label", str(tmp_path), "test_plot.png")
    assert file_path.exists()
