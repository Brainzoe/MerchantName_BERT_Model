# model/train_model.py

import pandas as pd
from datasets import Dataset
from sklearn.preprocessing import LabelEncoder
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import torch

# 1. Load data
df = pd.read_excel("Test mastersheet.xlsx")
df = df[['MERCHANT NAME', 'UNIFORM MERCHANT NAME', 'MERCHANT CATERGORY', 'MAIN SEGMENT', 'Priority Segment']].dropna()

# 2. Encode labels and text
le = LabelEncoder()
df['label'] = le.fit_transform(df['UNIFORM MERCHANT NAME'])
df['text_input'] = df['MERCHANT NAME'].astype(str).str.lower()

# 3. Convert to HuggingFace dataset
hf_ds = Dataset.from_pandas(df[['text_input', 'label']])

# 4. Tokenize
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize_fn(example):
    return tokenizer(example['text_input'], truncation=True, padding='max_length', max_length=64)

tokenized_ds = hf_ds.map(tokenize_fn, batched=True)
split_ds = tokenized_ds.train_test_split(test_size=0.2)

# 5. Load model
num_labels = df['label'].nunique()
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=num_labels)

# 6. Train model
training_args = TrainingArguments(
    output_dir="./merchant_model",
    eval_strategy="epoch",
    num_train_epochs=3,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=64,
    logging_dir="./logs"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=split_ds["train"],
    eval_dataset=split_ds["test"],
    tokenizer=tokenizer
)

print("🔧 Training model...")
trainer.train()
print("✅ Training complete!")

# 7. Save model & tokenizer
model.save_pretrained("merchant_model")
tokenizer.save_pretrained("merchant_model")

# 8. Save label encoder
import joblib
joblib.dump(le, "merchant_model/label_encoder.pkl")

print("✅ Model, tokenizer, and label encoder saved to /merchant_model")
