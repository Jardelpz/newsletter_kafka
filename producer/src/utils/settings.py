from src import __version__


ELASTIC_APM = {
    'SERVER_URL': 'http://localhost:8200',
    'SERVICE_NAME': "producer_kafka",
    'SERVICE_VERSION': __version__,
    'ENVIRONMENT': 'local',
    'TRANSACTIONS_IGNORE_PATTERNS': ['/hc']
}

