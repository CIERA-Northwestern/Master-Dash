# Get the config file.
import os

# Ensure the repository is added to the path
# This should typically be accessible post pip-installation
# But we add it to the path because when hosted on the web
# that doesn't work necessarily.
import sys
root_dir = os.path.dirname(os.path.dirname(__file__))
if root_dir not in sys.path:
    sys.path.append(root_dir)

# Call the main function.
# Change the import here to whatever page you want to load.
import importlib
from dash_lib.pages import base_page
importlib.reload(base_page)
base_page.main(root_dir)
