from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from redis_database import Database


class Item(BaseModel):
    url: str


app = FastAPI()
URL = 'http://95.217.188.38:8889/'


@app.get('/{item_id}')
def redirect(item_id: int):
    db = Database()
    db.connect()

    url = db.get(item_id)
    return RedirectResponse(url)


@app.post('/put/')
def put_item(item: Item):
    db = Database()
    db.connect()

    item_dict = item.dict()
    idx = db.put(item.url)
    item_dict.update({'Yflshort_url': URL + idx})
    return item_dict
