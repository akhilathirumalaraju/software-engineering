import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

# Your Hugging Face API token
API_TOKEN = "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"  # Replace this with your Hugging Face API token

# Hugging Face Inference API URL
API_URL = "https://huggingface.co/Akhilathirumalaraju/telugu_summarization_model" # Replace with your model's URL

# Set up the headers with your Hugging Face API token
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}
@app.route("/")
def index():
    return "Welcome to the Telugu Summarization API!"

@app.route("/summarize", methods=["POST"])
def summarize():
    print("nocfg")
    data = request.get_json()  # Get JSON data from the request
    input_text = data.get("text", "")  # Extract text from the data

    if not input_text:
        return jsonify({"error": "No input text provided"}), 400  # Handle case if no text is provided

    # Prepare the payload for the Hugging Face Inference API
    payload = {
        "inputs": input_text,
    }

    # Send the request to Hugging Face's Inference API
    response = requests.post(API_URL, headers=headers, json=payload)
    print("HF response:", response.text)

    # Handle the response
    if response.status_code == 200:
        result = response.json()
        summary = result[0]["summary_text"]  # Get the summary from the API response
        return jsonify({"summary": summary})  # Return the summary in the response
    else:
        return jsonify({"error": "Failed to get response from Hugging Face API"}), response.status_code

if __name__ == "__main__":
    app.run(debug=True,port=5000)
