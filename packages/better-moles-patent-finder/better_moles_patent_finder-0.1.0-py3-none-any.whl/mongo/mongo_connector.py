from pymongo import MongoClient

from mongo.mongo_configs import MongoConnectionConfig


class MongoConnector:
    """
    A connector class for MongoDB that handles connections, database, and collection access.

    Attributes:
        config (MongoConnectionConfig): Configuration object for MongoDB connection.
        client (MongoClient): The MongoDB client instance.
        db (Database): The MongoDB database instance.
        collection (Collection): The MongoDB collection instance.

    Methods:
        connect(): Establishes a connection to the MongoDB server.
        close(): Closes the connection to MongoDB.
    """

    def __init__(self, config: MongoConnectionConfig):
        """
        Initializes MongoConnector with the provided configuration.

        Args:
            config (MongoConnectionConfig): The configuration object for MongoDB.
        """
        self.config = config
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        """
        Establishes a connection to the MongoDB server and sets the database and collection.

        Raises:
            ConnectionError: If the connection to MongoDB fails.
        """
        if self.client is None:
            try:
                self.client = MongoClient(self.config.get_connection_uri())
                self.db = self.client[self.config.db_name]
                self.collection = self.db[self.config.collection]
                print(f"Connected to MongoDB: {self.config.get_connection_uri()}")
            except Exception as e:
                raise ConnectionError(f"Error connecting to MongoDB: {e}")

    def close(self):
        """
        Closes the connection to MongoDB.
        """
        if self.client is not None:
            self.client.close()
            self.client = None
