import logging.config

TG_TOKEN = '1849415465:AAF24O4D-shmTZXB9UJvoTGEYmfAUesr_zo'

LOGGING = {
    "disable_existing_loggers": True,
    'version': 1,
    'formatters' : {
        'verbose': {
            'format': '%(levelname)s %(module)s.%(funcName)s | %(asctime)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class' : 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers' : ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
logging.config.dictConfig(LOGGING)