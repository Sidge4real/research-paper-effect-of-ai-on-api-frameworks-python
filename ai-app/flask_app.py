from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv('MONGODB_URI'))
app = Flask(__name__)
db = client.researchDB.flask

@app.route('/posts', methods=['GET'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    posts = list(db.find().skip((page-1)*10).limit(10))
    return jsonify([{**post, '_id': str(post['_id'])} for post in posts])

@app.route('/posts/<id>', methods=['GET'])
def get_post(id):
    post = db.find_one({'_id': id})
    return jsonify({**post, '_id': str(post['_id'])}) if post else ('', 404)

@app.route('/posts', methods=['POST'])
def create_post():
    post = request.json
    result = db.insert_one(post)
    return jsonify({'_id': str(result.inserted_id)}), 201

# ... PUT and DELETE endpoints follow similar pattern ...

# Load model at startup
summarizer = pipeline("summarization", 
                     model="facebook/bart-large-cnn",
                     torch_dtype=torch.float16)

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
            
        summary = summarizer(text, 
                            max_length=150, 
                            min_length=40, 
                            do_sample=False)
        
        return jsonify({
            'summary': summary[0]['summary_text']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)