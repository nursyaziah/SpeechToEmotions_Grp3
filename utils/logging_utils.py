from pathlib import Path
from datetime import datetime
import logging

def setup_logging():
    log_dir = Path('./logs')
    log_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"PROCESSING_DATASET_{timestamp}.log"

    logging.basicConfig(
        level = logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)