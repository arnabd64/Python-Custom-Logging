# Python Custom Logger

# Overview

This repository serves as a simple guide for the readers to build custom loggers for their python projects. Logging is a key feature that should be incorporated into applications which can help us to monitor our applications. There are several libraries and framework available for python which can help developers integrate logging but I prefer to use the inbuilt `logging` module because it reduces 3rd party package dependencies. Although sometimes when using the `logging` module, we may need to develop our custom logging logic to integrate with 3rd party services like SQL Databases or other logging servers.

# Python Logging Pipeline

Let's see an overview of Python's `logging` pipeline.

1. First we create a new **LogRecord** while executing `logger.info`, `logger.debug` or `logger.error`.
2. The `LogRecord` object is passed through an optional **Filter**. If the filter returns `True` then the `LogRecord` is forwarded in the pipeline else it is dropped.
3. Next step is to transform the `LogRecord` into a suitable format using the **Formatter**.
4. Finally the **Handler** dispatches or emits the formatted log to our desired location.

# Examples

## Basic Console Logging

The Console logs are the most simple form of logging that python by default provides to it's users. Everytime we log an event, we see the event in the terminal. The formatter converts the `LogRecord` instance into a plaintext string which the `StreamHandler` pushes to the terminal for the user to see.

## Structured Logging to SQLite Database

Structured logging is type of logging where the logs are **stored** in a predefined structure like JSON, XMLs, SQL Tables etc. Structured Logging has been to be useful for debugging applications in a production environment. 

For this example we will be needed **SQLAlchemy** which is a popular ORM framework for Database operations. You can refer to [sqlite_logger](./custom_loggers/sqlite_logger.py) for more details. For this example we have to create a database model for storing logs.

We must define a custom formatter named `SQLAlchemyFormatter` which converts a `LogRecord` instance into an instance of the SQLAlchemy data model. Then the `SQLAlchemyHandler` pushes the record to the SQLite Database.
