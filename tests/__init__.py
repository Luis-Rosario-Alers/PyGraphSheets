import sys
import os

# Add the directory containing the module to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Functionality', 'data_plotter')))

# Now you can import the module
from Functionality.data_plotter import plot_data