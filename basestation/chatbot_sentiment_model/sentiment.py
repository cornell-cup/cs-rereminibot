import pandas as pd
import numpy as np
import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, TrainingArguments, Trainer
from transformers import TextClassificationPipeline

df = pd.read_csv("training_data.tsv", sep="\t", header=None, names=["Statement","Category", "id"])
df.drop(columns=["id"], inplace=True)

def row_to_vector(label_str):
    vector = [0] * 28
    for label in label_str.split(","):
        if label.strip():
            label_int = int(label.strip())
            vector[label_int] = 1
    return vector

df["Label"] = df["Category"].apply(row_to_vector)

train_texts, test_texts, train_labels, test_labels = train_test_split(
    df["Statement"].tolist(), df["Label"].tolist(), test_size=0.2, random_state=42
)

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
train_statements = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
test_statements = tokenizer(test_texts, truncation=True, padding=True, max_length=128)

class MultiLabelDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx], dtype=torch.float)
        return item
    
train_dataset = MultiLabelDataset(train_statements, train_labels)
test_dataset = MultiLabelDataset(test_statements, test_labels)


model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=28, problem_type="multi_label_classification")

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    eval_strategy="epoch",
    report_to="none"
)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

trainer.train()
model.save_pretrained("./sentiment-model")
tokenizer.save_pretrained("./sentiment-model")
