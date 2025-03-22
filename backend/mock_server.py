from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "Fake News Detection API Mock Server is running",
        "model_loaded": True
    })

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({
            "status": "error",
            "message": "No text provided for analysis"
        }), 400
    
    # Get the news text from the request
    news_text = data['text']
    
    if not news_text.strip():
        return jsonify({
            "status": "error",
            "message": "Empty text provided"
        }), 400
    
    # Generate a random prediction (for mock purposes)
    is_fake = random.random() > 0.5
    confidence = random.uniform(0.7, 0.99)
    
    return jsonify({
        "status": "success",
        "prediction": "FAKE" if is_fake else "REAL",
        "confidence": float(confidence),
        "processed_at": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 