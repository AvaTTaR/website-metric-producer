import os

kafka_producer_config_params = {
    'bootstrap_servers': os.getenv('KAFKA_HOST_PORT')
}

kafka_consumer_config_params = {
    'auto_offset_reset': "earliest",
    'bootstrap_servers': os.getenv('KAFKA_HOST_PORT'),
    'client_id': os.getenv('KAFKA_CLIENT_ID'),
    'group_id': os.getenv('KAFKA_GROUP_ID')
}

kafka_topic = os.getenv('KAFKA_TOPIC')

postgres_connection_config_params = {
    'user': os.getenv('POSTGRES_DB_USER'),
    'password': os.getenv('POSTGRES_DB_PASSWORD'),
    'host': os.getenv('POSTGRES_DB_HOST'),
    'port': os.getenv('POSTGRES_DB_PORT'),
    'database': os.getenv('POSTGRES_DB_DATABASE'),
}

integration_mode = False

target_website_simulator_url = os.getenv('TARGET_SIMULATOR_HOST')
