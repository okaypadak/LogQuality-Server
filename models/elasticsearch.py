from elasticsearch_dsl import Document, Date, Text, Keyword
from elasticsearch_dsl.connections import connections
from datetime import datetime

class LogEntry(Document):
    timestamp = Date()
    level = Keyword()
    logId = Keyword()
    message = Text()
    threadName = Keyword()
    loggerName = Keyword()
    exception = Text()

    class Index:
        name = 'log_entries'