
import time
from concurrent.futures import as_completed, ThreadPoolExecutor
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from reader.ProjectList import project
from util.LogProcess import logger


class ElasticSearchReader:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])


    def streaming(self, proje):

        while True:
            
            today = datetime.now().strftime("%Y-%m-%d")
            start_of_day = today + "T00:00:00"
            end_of_day = today + "T23:59:59"

            query = {
                "query": {
                    "range": {
                        "@timestamp": {
                            "gte": start_of_day,
                            "lte": end_of_day
                        }
                    }
                }
            }

            logs = []


            logs = scan(self.es, query=query, index="testapplogs")

            for log in logs:
                print(log['_source'])

            time.sleep(1)



    def start(self):

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.streaming, proje): proje for proje in project.list()}

            for future in as_completed(futures):
                try:
                    if future.exception() is None:  # Hata yoksa
                        proje_id, logs = future.result()

                        if logs is not None:
                            logger.info("geldi")
                            # self.ayristir(proje_id, lines)

                except Exception as e:
                    logger.error(f"Hata: {e}")
