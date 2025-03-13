import pandas as pd
import numpy as np
import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, TrainingArguments, Trainer
from transformers import TextClassificationPipeline

df = pd.read_csv("Chatbot_Sentiment_Data.csv")
label_mapping = {-5: 0, -4: 1, -3: 2, -2: 3, -1: 4, 0: 5, 1: 6, 2: 7, 3: 8, 4: 9}
df["Label"] = df["Category"].map(label_mapping)
# Train-Test Split
train_texts, test_texts, train_labels, test_labels = train_test_split(
    df["Statement"].tolist(), df["Label"].tolist(), test_size=0.2, random_state=42
)

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=128)

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


model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=10)
model.eval()

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    evaluation_strategy="epoch",
    report_to="none"
)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)
trainer.train()
model.save_pretrained("./chatbot-sentiment-model")

pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=False)
x = pipe(["Hello I'm so happy. I want to go outside and enjoy the sun. The lovely weather inspires me."])
print (x)







