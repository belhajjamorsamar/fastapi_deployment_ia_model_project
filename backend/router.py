from fastapi import FastAPI
from pydantic import  BaseModel 
#le modele pydantic definit la structures des donneés 
# Codes d'état HTTP courants :
# - 200 OK : Succès par défaut
# - 201 Created : Objet créé avec succès
# - 400 Bad Request : Mauvaise requête
# - 404 Not Found : Ressource non trouvée
# - 500 Internal Server Error : Erreur interne du serveur 
app=FastAPI()
db={}

@app.get('/item/{item_id}')#@app.get definit l'endpoint , {item_id} est une parametres de chemin qui sera passé à la fonction read_item
async def read_item(item_id: int): 
    if item_id ==4242 : # an invalid ordeer number
        raise HTTPException(status_code=404, detail='Item not found')
    return {"item_id":item_id}


class Item(BaseModel):
    name: str
    price: float

@app.post("/items", status_code=201)
# 1. FastAPI reçoit le JSON envoyé dans le corps de la requête HTTP (Request Body).
def create_item(item:Item):
    # 3. `model_dump()` transforme cet objet Pydantic en dictionnaire Python classique :
    db[item.name]=item.model_dump()

    return {"message":f"created item {item.name} with price {item.price}"}