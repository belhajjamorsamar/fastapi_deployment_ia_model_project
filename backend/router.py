from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic import ValidationError
import joblib
import uvicorn

app = FastAPI()
db = {}

@app.get('/item/{item_id}')
async def read_item(item_id: int): 
    if item_id == 4242: # an invalid order number
        raise HTTPException(status_code=404, detail='Item not found')
    return {"item_id": item_id}


class Item(BaseModel):
    name: str
    price: float

class User (BaseModel):
    username: str
    email: str
    age: int

@app.post("/items", status_code=201)
def create_item(item: Item):
    db[item.name] = item.model_dump()
    return {"message": f"created item {item.name} with price {item.price}", "status_code": 201}


# Pydantic model for penguin prediction features
class PenguinFeatures(BaseModel):
    culmen_length_mm: float
    culmen_depth_mm: float
    flipper_length_mm: float
    body_mass_g: float


# Load the trained model (corrected filename)
model = joblib.load("penguin_classifier.pkl")

@app.post("/predict") 
def predict(features: PenguinFeatures):
    # Prepare data for prediction
    data = [[
        features.culmen_length_mm, 
        features.culmen_depth_mm, 
        features.flipper_length_mm, 
        features.body_mass_g
    ]]
    prediction = model.predict(data)
    return {"prediction": prediction[0]}


@app.post("/users", response_model=User)
async def create_user(user:User):
    return user
try:
    invalid_user=User(username="john_doe", email="john@example.com", age=18)
    print("invalid_user:", invalid_user)
except ValidationError as e:
    print(f"Validation error: {e}")
    
class CommentText(BaseModel):
    text: str

@app.post("/analyze_text")
def analyze_text(comment:CommentText):
    forbiden=["spam", "hate","free","fake","sign up"]
    text_lower=comment.lower()
    issues = [word for word in forbiden
              if word in text_lower]
    return {
        "issues" : issues,
        "needs_moderation" : "len(issues)"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8002)