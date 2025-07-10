# app.py

import os
import shutil
import pandas as pd
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from model.utils import MerchantModel

# Initialize FastAPI app
app = FastAPI()

# Load model
merchant_model = MerchantModel()

# Mount static UI directory
app.mount("/", StaticFiles(directory="static", html=True), name="static")


# Root endpoint
@app.get("/")
def home():
    return {"message": "Merchant Uniform Name API is running."}


# Prediction endpoint for raw merchant name
class MerchantInput(BaseModel):
    merchant_name: str

@app.post("/predict")
def predict_merchant(input_data: MerchantInput):
    result = merchant_model.predict(input_data.merchant_name)
    return result


# CSV upload + batch prediction endpoint
@app.post("/upload-csv/")
def upload_csv(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    temp_file = os.path.join("uploads", file.filename)
    
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = pd.read_csv(temp_file)
    if 'merchant_name' not in df.columns:
        return {"error": "CSV must have a 'merchant_name' column"}

    results = []
    for name in df['merchant_name']:
        pred = merchant_model.predict(name)
        results.append(pred)

    result_df = pd.DataFrame(results)
    output_file = temp_file.replace(".csv", "_predicted.csv")
    result_df.to_csv(output_file, index=False)

    return {
        "message": "Prediction completed successfully.",
        "download_url": f"/download/{os.path.basename(output_file)}"
    }


# Endpoint to download predicted file
@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join("uploads", filename)
    return FileResponse(path=file_path, filename=filename, media_type='text/csv')



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
