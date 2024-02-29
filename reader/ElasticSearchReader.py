from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

class ElasticSearchReader:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def streaming(self, proje):
        logs = []
        for success, info in streaming_bulk(
                client=es,
                index=gelen['index_name'],

                query={"query": {"range": {"@timestamp": {"gte": "now-1s"}}}}
        ):
            if not success:
                print(f'Error indexing document: {info}')
            else:
                log_dict = info['index']['_source'].to_dict()
                logs.append(log_dict)

        return gelen['proje_id'], logs


    def start(self):

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.streaming, proje): proje for proje in project.list()}

            for future in as_completed(futures):
                try:
                    if future.result() is not None:

                        proje_id, lines = future.result()

                        if proje_id is not None:

                            self.ayristir(proje_id, lines)

                except RuntimeError as e:
                    logger.error(f"Hata: Future doğru sonuç türetmedi")