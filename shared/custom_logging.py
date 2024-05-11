import os
import json
import logging.config

def setup_logging():
    # Define the path to the logging configuration file
    config_path = os.path.join(os.path.dirname(__file__), 'logging_config.json')

    # Load the logging configuration from the JSON file
    with open(config_path, 'rt') as f:
        config = json.load(f)

    # Use dictConfig to apply the logging configuration
    logging.config.dictConfig(config)
