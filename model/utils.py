# model/utils.py (updated)
import torch
import pandas as pd
import joblib
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class MerchantModel:
    def __init__(self, model_path="merchant_model"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.eval()

        # Load label encoder
        self.label_encoder = joblib.load(f"{model_path}/label_encoder.pkl")

        # Load merchant metadata
        df = pd.read_excel("mastersheet.xlsx")
        df = df[['MERCHANT NAME', 'UNIFORM MERCHANT NAME', 'MERCHANT CATERGORY', 'MAIN SEGMENT', 'Priority Segment']].dropna()
        self.uniform_lookup = df.drop_duplicates(subset=['UNIFORM MERCHANT NAME']) \
            .set_index('UNIFORM MERCHANT NAME')[['MERCHANT CATERGORY', 'MAIN SEGMENT', 'Priority Segment']]

    def predict(self, merchant_name_raw):
        text = merchant_name_raw.strip().lower()
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=64)
        with torch.no_grad():
            outputs = self.model(**inputs)
            pred_label = torch.argmax(outputs.logits, dim=1).item()

        uniform_name = self.label_encoder.inverse_transform([pred_label])[0]
        details = self.uniform_lookup.loc[uniform_name]

        return {
            "Uniform Merchant Name": uniform_name,
            "Merchant Category": details['MERCHANT CATERGORY'],
            "Main Segment": details['MAIN SEGMENT'],
            "Priority Segment": details['Priority Segment']
        }
