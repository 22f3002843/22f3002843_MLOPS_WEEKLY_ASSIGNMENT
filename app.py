
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
def read_root():
    return {"message": "Iris prediction API"}

@app.post("/predict")
def predict(data: IrisInput):
    if data.petal_length < 2.45:
        prediction = "setosa"
    elif data.petal_width < 1.75:
        prediction = "versicolor"
    else:
        prediction = "virginica"
    return {"prediction": prediction}