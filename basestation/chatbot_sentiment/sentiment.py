import torch
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, TrainingArguments, Trainer
from sklearn.model_selection import train_test_split
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Load Dataset
df = pd.read_csv("chatbot_sentiment_data.csv")
label_mapping = {-5: 0, -4: 1, -3: 2, -2: 3, -1: 4, 0: 5, 1: 6, 2: 7, 3: 8, 4: 9}
df["Label"] = df["Category"].map(label_mapping)

# Train-Test Split
train_texts, test_texts, train_labels, test_labels = train_test_split(
    df["Statement"].tolist(), df["Label"].tolist(), test_size=0.2, random_state=42
)

# Tokenization
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=128)

# Dataset Class
class SentimentDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

train_dataset = SentimentDataset(train_encodings, train_labels)
test_dataset = SentimentDataset(test_encodings, test_labels)

# Load Model
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=10)
model.eval()

# Training
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    evaluation_strategy="epoch"
)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)
trainer.train()
model.save_pretrained("./chatbot-sentiment-model")

# Inference API with FastAPI
app = FastAPI()
class TextInput(BaseModel):
    text: str

@app.post("/predict")
def predict_sentiment(input_data: TextInput):
    inputs = tokenizer(input_data.text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    return {"predicted_sentiment": list(label_mapping.keys())[list(label_mapping.values()).index(predicted_class)]}

# Run API Server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
