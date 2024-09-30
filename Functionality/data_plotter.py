import logging
import matplotlib.pyplot as plt
import os

logger = logging.getLogger(__name__)


def plot_data(data, plot_settings, label, directory, file_name, axes, graph_type, x_col_indices, y_col_indices):
    for sheet_name, sheet_data in data.items():
        for x_col_index in x_col_indices:
            for y_col_index in y_col_indices:
                if len(sheet_data) <= max(x_col_index, y_col_index):
                    continue  # Skip if there are not enough columns

                x_data = sheet_data[x_col_index][1:]  # Specified column as x-axis, skip header
                y_data = sheet_data[y_col_index][1:]  # Specified column as y-axis, skip header

                # Convert x_data and y_data to float for sorting
                x_data = list(map(float, x_data))
                y_data = list(map(float, y_data))

                # Sort the data based on x_data
                sorted_data = sorted(zip(x_data, y_data))
                x_data, y_data = zip(*sorted_data)

                if graph_type == "Line":
                    axes.plot(
                        x_data,
                        y_data,
                        label=f"{sheet_name} {label} (X: {x_col_index}, Y: {y_col_index})",
                        linestyle=plot_settings.get("line_style", "-"),
                        color=plot_settings.get("line_color", "blue"),
                        linewidth=plot_settings.get("line_width", 1),
                        marker=plot_settings.get("marker", "")
                    )
                elif graph_type == "Bar":
                    axes.bar(
                        x_data,
                        y_data,
                        label=f"{sheet_name} {label} (X: {x_col_index}, Y: {y_col_index})",
                        color=plot_settings.get("line_color", "blue")
                    )
                elif graph_type == "Scatter":
                    axes.scatter(
                        x_data,
                        y_data,
                        label=f"{sheet_name} {label} (X: {x_col_index}, Y: {y_col_index})",
                        color=plot_settings.get("line_color", "blue"),
                        marker=plot_settings.get("marker", "o")
                    )

    axes.set_xlabel(plot_settings["xlabel"])
    axes.set_ylabel(plot_settings["ylabel"])
    axes.set_title(plot_settings["title"])
    axes.legend(
        loc=plot_settings["legend_loc"],
        fontsize=plot_settings["legend_fontsize"],
        title=plot_settings["legend_title"],
        title_fontsize=plot_settings["legend_title_fontsize"],
        shadow=plot_settings["legend_shadow"],
        frameon=plot_settings["legend_frameon"]
    )
    if plot_settings.get("grid", False):
        axes.grid(True)

    return axes