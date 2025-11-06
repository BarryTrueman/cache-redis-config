import os
import logging
import redis
import yaml

class Config:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.file_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logging.error(f"Config file {self.file_path} not found")
            return None
        except yaml.YAMLError as e:
            logging.error(f"Error parsing config file {self.file_path}: {e}")
            return None

    def get_config(self, key, default=None):
        config = self.config.get(key, default)
        if config is None:
            logging.error(f"Missing config key {key}")
            return default
        return config

def get_redis_client(config):
    host = config.get('redis', {}).get('host', 'localhost')
    port = config.get('redis', {}).get('port', 6379)
    db = config.get('redis', {}).get('db', 0)
    return redis.Redis(host=host, port=port, db=db)

def get_cache_config(config):
    return config.get('cache', {})