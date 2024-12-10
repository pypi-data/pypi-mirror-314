"""
ckey placeholder - OpenFEC API client for researching the political spending of executives.

Copyright (c) 2024 Justin G. Davis
This module is released under the MIT License: https://www.opensource.org/licenses/mit-license.php
"""

def run(
    data_path: str,
    id_column: str,
    name_column: str,
    company_column: str,
    year_column: str,
    key: str,
    upgraded_key: bool = False):
    
    import pandas as pd
    import logging
    import requests
    import os
    import time
    from ThreadPoolExecutorPlus import ThreadPoolExecutor
    from .utils.aggregators import compress_requests, aggregate
    from .utils.api import process_batch, log_progress, lookup
    from .utils.formatters import input_formatter
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='\n%(asctime)s - %(levelname)s:\n%(message)s\n',
        datefmt='%Y-%m-%d %H:%M:%S')
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    for handler in root_logger.handlers:
        handler.setLevel(logging.INFO)
    
    logging.info(
        'Thank you for using ckey.\n\n'
        'The full version will be available\n'
        'using pip install ckey once\n'
        '"Measuring Executive Political\n'
        'Ideology with Ckey: A Methodology,\n'
        'Tool, and Guide" is accepted for\n'
        'publication.')
