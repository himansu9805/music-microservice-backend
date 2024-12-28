"""Mongo Connection Module."""

import logging

from pymongo import MongoClient
from pymongo.errors import ConfigurationError
from pymongo.errors import ConnectionFailure

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class MongoConnect:
    """
    Mongo Connection Class.

    This class is responsible for establishing a connection to a MongoDB
    database.

    Attributes:
        uri (str): The URI of the MongoDB server.
        database (str): The name of the database to connect to.
        collection (str): The name of the collection to connect to.

    Methods:
        _connect(): Establishes a connection to the MongoDB server.
        get_collection(): Returns the specified collection from the database.
    """

    def __init__(self, uri, database, collection):
        """
        Initializes the MongoDB connection parameters and establishes a
        connection.
        Args:
            uri (str): The MongoDB connection URI.
            database (str): The name of the MongoDB database to connect to.
            collection (str): The name of the MongoDB collection to connect to.
        """
        self.uri = uri
        self.database = database
        self.collection = collection
        self.client = None
        self._connect()

    def _connect(self):
        """
        Establishes a connection to the MongoDB server using the provided
        host, port, user, and password.

        Raises:
            pymongo.errors.ConnectionFailure: If the connection to the MongoDB
            server fails.
            pymongo.errors.ConfigurationError: If there is an issue with the
            provided configuration.
        """
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Verify connection
            self.client.admin.command("ping")
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
        except ConfigurationError as e:
            logger.error(f"Configuration error: {e}")
            raise

    def get_collection(self):
        """
        Returns the specified collection from the database.

        Returns:
            Collection: The MongoDB collection object.
        """
        return self.client[self.database][self.collection]

    def close(self):
        """
        Closes the MongoDB connection.
        """
        self.client.close()
