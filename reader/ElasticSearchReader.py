from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

class ElasticSearchReader:
    def __init__(self, index_name):
        self.index_name = index_name
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def process_logs(self):
        for success, info in streaming_bulk(
            client=self.es,
            index=self.index_name,
            query={"query": {"range": {"@timestamp": {"gte": "now-1s"}}}}
        ):
            if not success:
                print(f'Error indexing document: {info}')
            else:
                log_dict = info['index']['_source'].to_dict()  # Log verisini Python sözlüğüne dönüştür
                print(log_dict)  # Dönüştürülmüş logu yazdır