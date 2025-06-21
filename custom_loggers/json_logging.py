import json
import logging
import uuid
from logging import Formatter, Handler, LogRecord
from pymongo import MongoClient


class JSONFormatter(Formatter):
    """
    The `JSONFormatter` transforms a `LogRecord` into a 
    python dictionary.
    """

    def format(self, record: LogRecord) -> dict:
        return {
            "id": str(uuid.uuid4()),
            "levelname": record.levelname,
            "timestamp": self.formatTime(record, self.datefmt),
            "message": record.getMessage(),
            "name": record.name,
            "module": record.module,
            "function": record.funcName,
            "lineno": record.lineno
        }


class MongoDBLogs(Handler):

    def __init__(self, client: MongoClient, collection: str, database = "Logs", level=logging.NOTSET):
        super().__init__(level=level)
        
        # link with collection
        self.coll = client[database][collection]


    def emit(self, record: LogRecord):
        return self.coll.insert_one(self.format(record))


if __name__ == '__main__':
    # connect to Mongo Database
    client = MongoClient("mongodb://username:password@localhost:27017/admin", connect=True)

    # build logger
    handler = MongoDBLogs(client, "events")
    handler.setFormatter(JSONFormatter())
    handler.setLevel(logging.INFO)

    logger = logging.getLogger('myLogger')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # test logging
    logger.info("INFO message")
    logger.warning("WARNING message")
    logger.error("ERROR message")
