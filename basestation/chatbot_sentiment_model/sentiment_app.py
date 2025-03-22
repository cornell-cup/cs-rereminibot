from flask import Flask, request, jsonify
from transformers import BertTokenizer, BertForSequenceClassification, TextClassificationPipeline

app = Flask(__name__)

tokenizer = BertTokenizer.from_pretrained("./chatbot-sentiment-model-s")
model = BertForSequenceClassification.from_pretrained("./chatbot-sentiment-model-s")

pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, top_k=1)

@app.route("/predict", methods = ["POST"])
def predict():
    data = request.get_json(force=True)
    text = data.get("text", "")
    prediction = pipe([text])
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=2300, debug=True)