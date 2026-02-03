from flask import Flask, render_template, request, jsonify
import json
import random
from nltk.tokenize import word_tokenize

app = Flask(__name__)

with open("intents.json") as f:
    intents = json.load(f)

def get_response(text):
    tokens = word_tokenize(text.lower())

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            pattern_tokens = word_tokenize(pattern.lower())
            if any(word in tokens for word in pattern_tokens):
                return random.choice(intent["responses"])

    return "Sorry, I didn't understand that."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message")
    reply = get_response(user_message)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
