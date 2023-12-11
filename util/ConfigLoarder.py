import yaml

# Global değişkenler
server_host = None
server_port = None
database_name = None

def read_config(file_path):

    global server_host, server_port, database_name

    with open(file_path, 'r') as file:
        config_data = yaml.safe_load(file)

    if 'server' in config_data:
        server_config = config_data['server']
        server_host = server_config.get('host', 'localhost')
        server_port = server_config.get('port', 8080)
        database_name = server_config.get('name', 'logstrack')

config_file_path = 'config.yml'

read_config(config_file_path)
