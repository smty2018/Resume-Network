from flask import Flask, request, jsonify
import requests
import google.generativeai as genai
import json

app = Flask(__name__)


genai.configure(api_key="geimini_api_key")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")



@app.route('/summarize/<data>', methods=['GET'])
def summarize(data):
    
    

    try:
        summary_response = model.generate_content(["Summarize this paragraph", data])
        return jsonify({"summary": summary_response.text})
    except Exception as e:
        app.logger.error(f"Error generating summary: {e}")
        return jsonify({"error": "Failed to generate summary"}), 500
    


if __name__ == '__main__':
    app.run(debug=True)
