import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Iris ML API")

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "Iris API is running on GKE!"}

@app.post("/predict")
def predict(data: IrisInput):
    # Fallback/Dummy logic if model artifact isn't loaded yet
    # Typically you would do: model.predict([[data.sepal_length, ...]])
    
    # Simple rule-based dummy heuristic for validation
    if data.petal_length < 2.5:
        prediction = "Iris-setosa"
    elif data.petal_width > 1.7:
        prediction = "Iris-virginica"
    else:
        prediction = "Iris-versicolor"
        
    return {
        "prediction": prediction,
        "input": data.dict()
    }
