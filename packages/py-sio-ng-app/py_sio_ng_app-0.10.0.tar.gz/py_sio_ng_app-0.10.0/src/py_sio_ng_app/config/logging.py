import logging.config


def initialize_logging(log_file_path):
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters':
            {
                'simple': {
                    'format': '[%(asctime)s.%(msecs)03d][%(name)s][%(threadName)s][%(levelname)s] %(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S'}
            },
        'handlers':
            {
                'console':
                    {
                        'class': 'logging.StreamHandler',
                        'level': 'DEBUG',
                        'formatter': 'simple',
                        'stream': 'ext://sys.stdout'},
                'file':
                    {
                        'class': 'logging.handlers.RotatingFileHandler',
                        'level': 'DEBUG',
                        'formatter': 'simple',
                        'filename': log_file_path,
                        'maxBytes': 10485760,
                        'backupCount': 20,
                        'encoding': 'utf8'
                    }
            },
        'root': {
            'level': 'DEBUG', 'handlers': ['console', 'file']
        }
    }
    logging.config.dictConfig(config)
