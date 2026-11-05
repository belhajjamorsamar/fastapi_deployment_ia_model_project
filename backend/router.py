from fastapi import FastAPI
from pydantic import  BaseModel 
#le modele pydantic definit la structures des donneés 

app=FastAPI()
db={}

@app.get('/item/{item_id}')#@app.get definit l'endpoint , {item_id} est une parametres de chemin qui sera passé à la fonction read_item
async def read_item(item_id: int): 
    return {"item_id":item_id}


class Item(BaseModel):
    name: str
    price: float

@app.post("/items", status_code=201)
def create_item(item:Item):
    db[item.name]=item.model_dump()
    db[item.price]=item.model_dump()

    return {"message":f"created item {item.name} with price {item.price}"}