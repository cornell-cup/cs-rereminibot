from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
sys.path.append('..')
from config import port_number
from ChatbotWrapper import ChatbotWrapper

app = Flask(__name__)
CORS(app)

wrapper = ChatbotWrapper()


@app.route("/predict", methods = ["POST"])
def predict():
    text = request.get_json(force=True).get("input")
    prediction = wrapper.predict_labels(text)
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=port_number, debug=False)

