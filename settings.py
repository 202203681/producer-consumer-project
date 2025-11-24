import os
from typing import Dict, Any


PROJECT_CONFIG: Dict[str, Any] = {
    "buffer_capacity": 10,
    "max_files": 20,
    "xml_directory": "xml_files",
    "log_directory": "logs",
    

    "threaded": {
        "produce_delay": 0.8,
        "consume_delay": 1.2,
        "runtime_duration": 30 
    },
    
 
    "socket": {
        "host": "127.0.0.1",
        "port": 9009,
        "delay": 1.0
    },
    
   
    "student": {
        "programmes": ["BSc IT", "Computer Science", "BSC", "BEng", "BIT"],
        "courses": ["CSC101", "CSC102", "MAT101", "ENG101", "ACS201", "CSC301", "NET202", "DB301"],
        "names": ["Lungelo", "Michael", "Aisha", "Sipho", "Nokuthula", "Thabo", "Zanele", "James"],
        "pass_threshold": 50.0
    }
}


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join('logs', 'producer_consumer.log'),
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        },
    }
}