import time
from concurrent.futures import as_completed, ThreadPoolExecutor
from datetime import datetime
from elasticsearch import Elasticsearch, NotFoundError
from elasticsearch.helpers import scan
from reader.ProjectList import project
from util.LogProcess import logger
import queue


class ElasticSearchReader:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
        self.log_queue = queue.Queue()
        self.seen_ids = set()

    def ayristir(self, log_id, logs):

        for log in logs:
            logSource = log['_source']
            if logSource['level'] in ('WARN','ERROR') and logSource['processed'] is False:
                logger.info(f"Warning log detected: {log}")
                try:
                    doc = self.es.get(index=log['_index'], id=log_id)
                    doc['_source']['processed'] = True
                    self.es.update(index=log['_index'], id=log_id, body={'doc': doc['_source']})
                except NotFoundError:
                    logger.error(f"Document with ID {log_id} not found.")

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

            logs = scan(self.es, query=query, index=proje['index_name'])

            for log in logs:
                log_id = log['_id']
                if log_id not in self.seen_ids:
                    self.seen_ids.add(log_id)
                    self.log_queue.put((log['_id'], log))

            time.sleep(1)

    def process_logs(self):
        while True:
            if not self.log_queue.empty():
                log_id, log = self.log_queue.get()
                self.ayristir(log_id, [log])
            else:
                time.sleep(1)

    def start(self):
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.streaming, proje): proje for proje in project.list()}
            executor.submit(self.process_logs)
