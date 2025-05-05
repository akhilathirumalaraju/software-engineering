import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

# Your Hugging Face API token
API_TOKEN = "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"  # Replace this with your Hugging Face API token

# Hugging Face Inference API URL
API_URL = "https://api-inference.huggingface.co/models/Akhilathirumalaraju/telugu_summary"

# Set up the headers with your Hugging Face API token
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

@app.route("/")
def index():
    return "Welcome to the Telugu Summarization API!"

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()  # Get JSON data from the request
        
        # Print received data for debugging
        print(f"Received data: {data}")
        
        input_text = data.get("text", "")  # Extract text from the data

        if not input_text:
            return jsonify({"error": "No input text provided"}), 400  # Handle case if no text is provided

        # Ensure text is in the correct format for the model
        # Most HF models expect text in the language they're trained for
        # Verify input is in Telugu if that's what the model expects

        # Prepare the payload for the Hugging Face Inference API
        payload = {
            "inputs": input_text,
            "options": {"wait_for_model": True}  # Wait for model to load if needed
        }

        print(f"Sending request to Hugging Face API: {payload}")

        # Send the request to Hugging Face's Inference API
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        # Print full response for debugging
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.text}")

        # Handle the response
        if response.status_code == 200:
            result = response.json()
            # Different models may have different response formats
            # Check the exact structure of the response
            if isinstance(result, list) and len(result) > 0 and "summary_text" in result[0]:
                summary = result[0]["summary_text"]
            else:
                # Handle different response formats
                print(f"Unexpected response format: {result}")
                summary = str(result)  # Convert to string as fallback
                
            return jsonify({"summary": summary})
        else:
            error_message = f"Failed with status {response.status_code}: {response.text}"
            print(f"API Error: {error_message}")
            return jsonify({"error": error_message}), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request to Hugging Face API timed out"}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Failed to connect to Hugging Face API"}), 502
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/test", methods=["GET"])
def test_connection():
    """Simple endpoint to test if the API token and connection are working"""
    try:
        # Use a simple request to check API access
        response = requests.get(
            "https://huggingface.co/api/models/Akhilathirumalaraju/telugu_summary", 
            headers=headers
        )
        if response.status_code == 200:
            return jsonify({"status": "success", "message": "Connection to Hugging Face API is working"})
        else:
            return jsonify({
                "status": "error", 
                "message": f"Failed to connect: {response.status_code}", 
                "details": response.text
            }), response.status_code
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)