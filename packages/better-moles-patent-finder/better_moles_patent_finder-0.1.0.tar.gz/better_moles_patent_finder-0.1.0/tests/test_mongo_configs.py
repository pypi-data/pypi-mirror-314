import pytest

from mongo.mongo_configs import MongoConnectionConfig


@pytest.mark.parametrize(
    "json_config, expected_values",
    [
        (
                {"host": "127.0.0.1", "db_name": "updated_db"},
                {"host": "127.0.0.1", "db_name": "updated_db", "port": 27017},
        ),
        (
                {"username": "new_user", "password": "new_pass"},
                {"username": "new_user", "password": "new_pass", "port": 27017},
        ),
    ],
)
def test_load_from_json(json_config, expected_values):
    config = MongoConnectionConfig(
        host="localhost",
        port=27017,
        db_name="test_db",
        collection="test_collection",
        username="user",
        password="pass",
        auth_db="admin",
    )
    config.load_from_json(json_config)

    for key, expected in expected_values.items():
        assert getattr(config, key) == expected


@pytest.mark.parametrize(
    "config_values, should_raise, missing_param",
    [
        (
                {
                    "host": "localhost",
                    "port": 27017,
                    "db_name": "test_db",
                    "collection": "test_collection",
                    "username": "user",
                    "password": "pass",
                    "auth_db": "admin",
                },
                False,
                None,
        ),
        (
                {
                    "host": "localhost",
                    "port": 27017,
                    "db_name": "test_db",
                    "collection": None,  # Missing parameter
                    "username": "user",
                    "password": "pass",
                    "auth_db": "admin",
                },
                True,
                "collection",
        ),
    ],
)
def test_check_parameters(config_values, should_raise, missing_param):
    config = MongoConnectionConfig(**config_values)

    if should_raise:
        with pytest.raises(ValueError, match=f"Missing parameter: {missing_param}"):
            config.check_parameters()
    else:
        try:
            config.check_parameters()  # Should not raise an exception
        except ValueError:
            pytest.fail("check_parameters raised ValueError unexpectedly!")


def test_get_connection_uri():
    config = MongoConnectionConfig(
        host="localhost",
        port=27017,
        db_name="test_db",
        collection="test_collection",
        username="user",
        password="pass",
        auth_db="admin",
    )
    assert config.get_connection_uri() == "mongodb://user:pass@localhost:27017/?authSource=admin"


if __name__ == "__main__":
    pytest.main()
