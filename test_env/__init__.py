import logging
import logging.config

import os

def init_logger(level=logging.DEBUG):
    results_dir = "results"
    log_file = os.path.join(results_dir, 'test.log')
    test_out_file = os.path.join(results_dir, 'test_output.log')

    cfg = {
        "version": 1.0,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
            "file": {
                "class": "logging.FileHandler",
                "mode": "w",
                "filename": log_file
            },
            "test_output": {
                "class": "logging.FileHandler",
                "mode": "w",
                "filename": test_out_file
            }
        },
        "loggers": {
            "": {
                "level": level,
                "handlers": ["console", "file"],
            },
            "test": {
                'level': level,
                'handlers': ['console', 'test_output'],
                'propagate': False
            }
        }
    }

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    logging.config.dictConfig(cfg)


