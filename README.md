# 🧠 Merchant Uniform Name Prediction API

This is a FastAPI-powered machine learning web service that predicts a **uniform merchant name** from noisy input merchant names using a fine-tuned BERT model.

## 🔍 Use Case
Many merchants operate under slightly different names across terminals, states, or banks. This app standardizes such entries to a single **uniform merchant name** and also returns:

- Merchant Category
- Main Segment
- Priority Segment

---

## 🚀 Features

✅ Upload `.csv` or `.xlsx` file with a `merchant_name` column  
✅ Predict standardized merchant names  
✅ Preview results  
✅ Download predicted results  
✅ Responsive, TailwindCSS-powered UI  
✅ API ready for integration

---

## 📂 Project Structure

merchant_api/
│
├── app.py # FastAPI entrypoint
├── model/
│ ├── init.py
│ ├── utils.py # Model loading & prediction
│ └── train_model.py # Model training script
├── merchant_model/ # Trained model (saved via HuggingFace)
├── tokenizer/ # Tokenizer folder
├── static/
│ └── index.html # Web UI with drag-and-drop upload
├── uploads/ # Auto-created file upload folder
├── requirements.txt
├── .gitignore
└── render.yaml # Render deployment config

yaml
Copy
Edit

---

## ⚙️ How to Use Locally

### 1. Clone and install dependencies
```bash
git clone https://github.com/yourusername/merchant-api.git
cd merchant-api
python -m venv .venv
source .venv/Scripts/activate  # Or .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
2. Run the app
bash
Copy
Edit
uvicorn app:app --reload
Access via: http://127.0.0.1:8000

☁️ Deploy on Render
This app is ready for Render. Just connect your GitHub repo and it will build & deploy automatically.

render.yaml
yaml
Copy
Edit
services:
  - type: web
    name: merchant-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app:app --host 0.0.0.0 --port 10000
    envVars:
      - key: PYTHON_VERSION
        value: 3.10
📤 Sample Upload Format
merchant_name
Shoprite Lagos
Shoprite Ikeja Mall
SHOPRITE SURULERE
Shoprite Victoria Island

📄 License
MIT License. Built with 💙 using FastAPI + Transformers + TailwindCSS.