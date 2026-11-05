from fastapi import FastAPI

app=FastAPI()

@app.get('/item/{item_id}')#@app.get definit l'endpoint , {item_id} est une parametres de chemin qui sera passé à la fonction read_item
async def read_item(item_id: int): 
    return {"item_id":item_id}
  