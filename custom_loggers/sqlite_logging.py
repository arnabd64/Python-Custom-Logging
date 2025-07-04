import logging
import uuid
from datetime import datetime
from logging import Formatter, Handler, LogRecord

from sqlalchemy import UUID, DateTime, Engine, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    ...


class Logs(Base):
    """
    SQLAlchemy data model for log events.

    Attributes:
        - id : UUIDv4 that acts as a primary key
        - level : Log Level (DEBUG, INFO, WARN, ERROR)
        - timestamp : Time when the event was recorded
        - message : Event Message
        - name : Name of the Logger
        - module : Python module generating the log
        - function : Name of the python function that generates the log
        - lineno : Line No where the log statement was found
    """
    __tablename__ = "logs"

    id: Mapped[UUID] = mapped_column(UUID(), primary_key=True, default=uuid.uuid4)
    level: Mapped[str] = mapped_column(String(10), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    message: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    module: Mapped[str] = mapped_column(String(255), index=True)
    function: Mapped[str] = mapped_column(String(255))
    lineno: Mapped[int] = mapped_column(Integer())


    def __repr__(self):
        return f"{self.level}: [{self.timestamp}] ({self.name}:{self.module}) {self.message}"


class SQLAlchemyFormatter(Formatter):
    """
    The `SQLAlchemyFormatter` transforms a `LogRecord` into
    a SQLAlchemy `Logs` Record.
    """

    def format(self, record: LogRecord) -> Logs:
        return Logs(
            level = record.levelname,
            message = record.getMessage(),
            name = record.name,
            module = record.module,
            function = record.funcName,
            lineno = record.lineno
        )
    

class SQLAlchemyHandler(Handler):
    """
    The `SQLAlchemyHandler` is responsible for sending the log events
    generated by a logger to a SQL Database.
    """

    def __init__(self, engine: Engine, level = logging.NOTSET):
        super().__init__(level=level)
        self.engine = engine


    def emit(self, record: LogRecord):
        """
        Uploads a `LogRecord` to a SQL Database.

        Args:
            - record (LogRecord) : Log event
        """
        Session = sessionmaker(self.engine)
        try:
            session = Session()
            session.add(self.format(record))
            session.commit()

        except Exception as e:
            session.rollback()
            self.handleError(self.format(record))

        finally:
            session.close()

    
if __name__ == '__main__':
    # create database engine
    engine = create_engine("sqlite:///logs.db", echo=False)

    # init the database
    Base.metadata.create_all(engine)

    # build the logger
    handler = SQLAlchemyHandler(engine)
    handler.setFormatter(SQLAlchemyFormatter())
    handler.setLevel(logging.INFO)
    
    logger = logging.getLogger('myLogger')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # test the logger
    logger.info("INFO message")
    logger.error("ERROR message")
    logger.warning("WARNING message")
