import logging.config

def setup_logging(default_level=logging.INFO):
    """Setup logging configuration."""
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': default_level,
            },
        },
        'root': {
            'handlers': ['console'],
            'level': default_level,
        },
    }
    logging.config.dictConfig(logging_config)
    logging.info("Logging is set up.")

# Example usage:
# setup_logging()