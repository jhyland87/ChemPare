"""General definitions to be used by any module"""

import os


__version__ = "v0.0"

# Directories
root_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
tests_dir = os.path.join(root_dir, "tests")
mock_data_dir = os.path.join(tests_dir, "mock_data")
