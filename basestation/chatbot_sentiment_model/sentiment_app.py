from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import numpy as np

app = Flask(__name__)
CORS(app)

tokenizer = BertTokenizer.from_pretrained("./sentiment-model")
model = BertForSequenceClassification.from_pretrained("./sentiment-model")
model.eval()

def predict_labels(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.sigmoid(logits)[0].cpu().numpy() 
    predicted_label = int(np.argmax(probs))
    return predicted_label if probs[predicted_label] > 0.07 else -1

@app.route("/predict", methods = ["POST"])
def predict():
    data = request.get_json(force=True)
    text = data.get("input")
    prediction = predict_labels(text)
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=2300, debug=False)

