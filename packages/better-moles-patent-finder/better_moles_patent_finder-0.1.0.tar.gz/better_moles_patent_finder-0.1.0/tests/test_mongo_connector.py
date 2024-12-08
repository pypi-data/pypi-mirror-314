from unittest.mock import patch, MagicMock

import pytest
from pymongo.errors import ConnectionFailure

from mongo.mongo_configs import MongoConnectionConfig
from mongo.mongo_connector import MongoConnector


@pytest.fixture
def mock_config():
    return MongoConnectionConfig(
        host="localhost",
        port=27017,
        db_name="test_db",
        collection="test_collection",
        username="user",
        password="pass",
        auth_db="admin",
    )


@pytest.fixture
def mock_mongo_client():
    with patch("mongo.mongo_connector.MongoClient") as mock:
        yield mock


def test_connect_success(mock_mongo_client, mock_config):
    mock_client_instance = MagicMock()
    mock_mongo_client.return_value = mock_client_instance
    connector = MongoConnector(mock_config)
    connector.connect()

    mock_mongo_client.assert_called_once_with(mock_config.get_connection_uri())
    assert connector.client == mock_client_instance
    assert connector.db == mock_client_instance[mock_config.db_name]
    assert connector.collection == connector.db[mock_config.collection]


@patch("mongo.mongo_connector.MongoClient")
def test_connect_failure(mock_mongo_client, mock_config):
    mock_mongo_client.side_effect = ConnectionFailure("Failed to connect")
    connector = MongoConnector(mock_config)

    with pytest.raises(ConnectionError, match="Error connecting to MongoDB: Failed to connect"):
        connector.connect()


@patch("mongo.mongo_connector.MongoClient")
def test_close(mock_mongo_client, mock_config):
    mock_client_instance = MagicMock()
    mock_mongo_client.return_value = mock_client_instance
    connector = MongoConnector(mock_config)
    connector.connect()
    connector.close()

    mock_client_instance.close.assert_called_once()
    assert connector.client is None


if __name__ == "__main__":
    pytest.main()
