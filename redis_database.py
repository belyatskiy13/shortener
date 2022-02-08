from dataclasses import dataclass
from typing import List, Union
from configparser import ConfigParser

import redis


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class Database(metaclass=Singleton):
    def __init__(self, config: str = 'config.ini'):
        conf = ConfigParser()
        conf.read(config)

        self.dictionary_name = conf['DATABASE']['dictionary_name']
        self.host = conf['DATABASE']['host']
        self.port = int(conf['DATABASE']['port'])
        self.db_id = int(conf['DATABASE']['db_id'])
        if conf['DATABASE']['password'] == '':
            self.password = None
        else:
            self.password = conf['DATABASE']['password']

    def connect(self) -> bool:
        if not hasattr(self, 'rc'):
            self.rc = redis.Redis(host=self.host, port=self.port, db=self.db_id, password=self.password)
            _ = self.rc.ping()

    def put(self, item: str) -> str:
        idx = self.rc.rpush(self.dictionary_name, item)
        idx -= 1
        return str(idx)

    def batch_put(self, items: List[str]) -> list[str]:
        with self.rc.pipeline() as pipe:
            processed_items = 0
            for item in items:
                pipe.rpush(self.dictionary_name, item)
                processed_items += 1
            item_ids = pipe.execute()
        item_ids = [id - 1 for id in item_ids]
        return item_ids, processed_items

    def get(self, idx: int) -> str:
        item = self.rc.lindex(self.dictionary_name, idx)
        if item:
            return item.decode('utf-8')
        else:
            return item

    def view_all(self, idx_start: int = 0, idx_end: int = -1) -> List[str]:
        items = self.rc.lrange(self.dictionary_name, idx_start, idx_end)
        items = [item.decode('utf-8') for item in items]
        return {'items': items}
