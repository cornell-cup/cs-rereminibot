from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import BertTokenizer, BertForSequenceClassification, TextClassificationPipeline
import os

app = Flask(__name__)
CORS(app)

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "chatbot-sentiment-model-s")

tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)

pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, top_k=1)

@app.route("/predict", methods = ["POST"])
def predict():
    data = request.get_json(force=True)
    text = data.get("text", "")
    prediction = pipe([text])
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=2300, debug=True)

