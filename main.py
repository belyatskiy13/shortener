from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from redis_database import Database


class Item(BaseModel):
    url: list[str]


app = FastAPI()
URL = 'http://95.217.188.38:8889/'


@app.get('/{item_id}')
def redirect(item_id: int):
    db = Database()
    db.connect()

    url = db.get(item_id)
    if not url:
        raise HTTPException(status_code=404, detail='Item not found')
    return RedirectResponse(url)


@app.get('/view_all/')
def view_all():
    db = Database()
    db.connect()

    return db.view_all()


@app.post('/put/')
def put_item(item: Item):
    db = Database()
    db.connect()

    item_dict = item.dict()

    if len(item.url) == 1:
        idx = db.put(item.url[0])
        idx = URL + idx
        processed_num = 1
    else:
        idx, processed_num = db.batch_put(item.url)
        idx = [URL + str(item) for item in idx]

    item_dict.update({'short_url': idx})
    item_dict.update({'processed_num': processed_num})
    return item_dict
