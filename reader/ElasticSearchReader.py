import re
import time
from concurrent.futures import as_completed, ThreadPoolExecutor
from elasticsearch import Elasticsearch, NotFoundError
from elasticsearch.helpers import scan
from models.OrtakBaglanti import session_scope
from reader.ProjectList import project
from repository.ArananKayitRepository import ArananKayitRepository
from repository.ArananRegex import ArananRegexManager
from repository.Takip import TakipManager
from repository.TakipZaman import TakipZamanManager
from util.LogProcess import logger
import queue
from util.ConfigLoarder import es_host, es_port

class ElasticSearchReader:
    def __init__(self):
        self.es = Elasticsearch([{'host': es_host, 'port': es_port, 'scheme': 'http'}])
        self.log_queue = queue.Queue()
        self.seen_ids = set()

    def ayristir(self, proje, log_id, logs):

        for log in logs:
            logSource = log['_source']
            #logger.info(f"log yakalandi: {log}")

            try:
                doc = self.es.get(index=log['_index'], id=log_id)
                exception = log['_source']['exception']

                if logSource['level'] in ('WARN', 'ERROR'):
                    if not exception:
                        self.belirli(proje, log)
                    else:
                        self.belirsiz(proje, log)

                doc['_source']['processed'] = True
                self.es.update(index=log['_index'], id=log_id, body={'doc': doc['_source']})

            except NotFoundError:
                logger.error(f"Document with ID {log_id} not found.")

    def belirli(self, proje, log_data):
        logger_name = log_data['_source']['loggerName']
        message = log_data['_source']['message']
        logId = log_data['_source']['logId']
        logTime = log_data['_source']['logTime']
        projeId = proje['proje_id']

        with session_scope() as session:
            kaydedilenTakip = TakipManager.create_or_update_takip(session, logger_name, message, projeId)
            TakipZamanManager.create_takip_zaman(session, logId, kaydedilenTakip.id, logTime)


    def belirsiz(self, proje, log_data):

        exception = log_data['_source']['exception']
        projeId = proje['proje_id']
        logTime = log_data['_source']['logTime']
        message = log_data['_source']['message']

        results = {}

        with session_scope() as session:
            regexs = ArananRegexManager.get_regexes_by_aranan_id(session, 1)

            sinif = re.findall(regexs['sınıf'], exception)[0]
            metod = re.findall(regexs['metod'], exception)[0]
            satir = re.findall(regexs['satır'], exception)[0]
            hata = re.findall(regexs['hata'], message)[0]

            ArananKayitRepository(session).add_aranan_kayit('sinif', sinif, 1)
            ArananKayitRepository(session).add_aranan_kayit('metod', metod, 1)
            ArananKayitRepository(session).add_aranan_kayit('satir_sayisi', satir, 1)
            ArananKayitRepository(session).add_aranan_kayit('hata', hata, 1)
            kaydedilenTakip = TakipManager.create_or_update_takip(session, sinif + '.' + metod, message, projeId)
            TakipZamanManager.create_takip_zaman(session, 0, kaydedilenTakip.id, logTime)



    def streaming(self, proje):
        while True:
            query = {
                "query": {
                    "term": {
                        "processed": {
                            "value": False
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

    def process_logs(self, proje):
        while True:
            if not self.log_queue.empty():
                log_id, log = self.log_queue.get()
                self.ayristir(proje, log_id, [log])
            else:
                time.sleep(1)

    def start(self):
        with ThreadPoolExecutor() as executor:
            futures = []
            for proje in project.list():
                futures.append(executor.submit(self.streaming, proje))
                futures.append(executor.submit(self.process_logs, proje))

            for future in as_completed(futures):
                result = future.result()
                logger.info(f"Task completed with result: {result}")
