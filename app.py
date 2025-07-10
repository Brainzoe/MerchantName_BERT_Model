# app.py

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})






# from fastapi import FastAPI
# from pydantic import BaseModel
# from model.utils import MerchantModel

# # Initialize app and model
# app = FastAPI()
# merchant_model = MerchantModel()

# # Define request schema
# class MerchantInput(BaseModel):
#     merchant_name: str

# @app.get("/")
# def home():
#     return {"message": "Merchant Uniform Name API is running."}

# @app.post("/predict")
# def predict_merchant(input_data: MerchantInput):
#     result = merchant_model.predict(input_data.merchant_name)
#     return result
