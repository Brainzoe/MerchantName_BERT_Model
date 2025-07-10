# app.py

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import shutil
import os
from model.utils import MerchantModel

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="static")

merchant_model = MerchantModel()

@app.post("/upload-csv/")
def upload_csv(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    temp_file = f"uploads/{file.filename}"

    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Support both .csv and .xlsx
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(temp_file)
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(temp_file)
        else:
            return {"error": "Only .csv and .xlsx files are supported"}
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}"}

    if 'merchant_name' not in df.columns:
        return {"error": "File must contain 'merchant_name' column"}

    results = []
    for name in df['merchant_name']:
        pred = merchant_model.predict(name)
        results.append(pred)

    result_df = pd.DataFrame(results)
    output_file = temp_file.replace(".csv", "_predicted.csv").replace(".xlsx", "_predicted.csv")
    result_df.to_csv(output_file, index=False)

    # Preview only first 10 rows
    preview = result_df.head(10).to_dict(orient="records")
    return {
        "message": "Prediction completed",
        "download_url": f"/download/{os.path.basename(output_file)}",
        "preview": preview
    }

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = f"uploads/{filename}"
    return FileResponse(path=file_path, filename=filename, media_type='text/csv')
from fastapi import File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import shutil
import os
from model.utils import MerchantModel

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="static")

merchant_model = MerchantModel()

@app.post("/upload-csv/")
def upload_csv(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    temp_file = f"uploads/{file.filename}"

    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Support both .csv and .xlsx
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(temp_file)
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(temp_file)
        else:
            return {"error": "Only .csv and .xlsx files are supported"}
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}"}

    if 'merchant_name' not in df.columns:
        return {"error": "File must contain 'merchant_name' column"}

    results = []
    for name in df['merchant_name']:
        pred = merchant_model.predict(name)
        results.append(pred)

    result_df = pd.DataFrame(results)
    output_file = temp_file.replace(".csv", "_predicted.csv").replace(".xlsx", "_predicted.csv")
    result_df.to_csv(output_file, index=False)

    # Preview only first 10 rows
    preview = result_df.head(10).to_dict(orient="records")
    return {
        "message": "Prediction completed",
        "download_url": f"/download/{os.path.basename(output_file)}",
        "preview": preview
    }

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = f"uploads/{filename}"
    return FileResponse(path=file_path, filename=filename, media_type='text/csv')
