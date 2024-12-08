from dataclasses import dataclass


@dataclass
class MongoConnectionConfig:
    host: str = "localhost"
    port: int = 27017
    db_name: str = ""
    collection: str = ""
    username: str = ""
    password: str = ""
    auth_db: str = "admin"

    def load_from_json(self, json_config):
        for param, value in json_config.items():
            if param in self.__dict__:
                expected_type = type(self.__dict__[param])
                if not isinstance(value, expected_type) and value is not None:
                    raise TypeError(f"Expected type {expected_type} for '{param}', got {type(value)}")
                self.__dict__[param] = value

    def check_parameters(self):
        for param in self.__dict__.keys():
            if self.__dict__[param] is None:
                raise ValueError(f"Missing parameter: {param}")

    def get_connection_uri(self) -> str:
        auth = f"{self.username}:{self.password}" if self.username and self.password else ""
        return f"mongodb://{auth}@{self.host}:{self.port}/?authSource={self.auth_db}"
