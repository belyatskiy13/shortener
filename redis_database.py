from dataclasses import dataclass
from typing import List, Union

import redis


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            print('class instance exists')
        return cls._instance


@dataclass
class Database(metaclass=Singleton):
    dictionary_name: str = 'links'
    host: str = 'localhost'
    port: int = 6379
    db_id: int = 0
    password: Union[str, None] = None

    def connect(self) -> bool:
        if not hasattr(self, 'rc'):
            self.rc = redis.Redis(host=self.host, port=self.port, db=self.db_id, password=self.password)
            _ = self.rc.ping()
        else:
            print('Connection exists')
        return True

    def put(self, item: str) -> str:
        idx = self.rc.rpush(self.dictionary_name, item)
        idx -= 1
        return str(idx)

    def batch_put(self, items: List[str]) -> List[str]:
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
        return item.decode('utf-8')

    def view_all(self, idx_start: int = 0, idx_end: int = -1) -> List[str]:
        items = self.rc.lrange(self.dictionary_name, idx_start, idx_end)
        items = [item.decode('utf-8') for item in items]
        return items
