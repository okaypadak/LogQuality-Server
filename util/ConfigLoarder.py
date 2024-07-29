import yaml

# Global değişkenler
postgres_host = None
postgres_port = None
database_name = None
es_host = None
es_port = None

def read_config(file_path):

    global postgres_host, postgres_port, database_name, es_host, es_port

    with open(file_path, 'r') as file:
        config_data = yaml.safe_load(file)

        porstgres_config = config_data['postgres']
        postgres_host = porstgres_config.get('host', 'localhost')
        postgres_port = porstgres_config.get('port', 5432)
        database_name = porstgres_config.get('name', 'logquality')

        es_config = config_data['elasticsearch']
        es_host = es_config.get('host', 'localhost')
        es_port = es_config.get('port', 9400)

config_file_path = 'config.yml'

read_config(config_file_path)