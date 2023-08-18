from flask import Flask, request, jsonify
from Book_recommender import *
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Routes 

@app.route('/', methods=['GET'])
def main_home():
    return jsonify({ "message": "Welcome" })


@app.route('/api', methods=['GET'])
def home():
    return jsonify({ 
                    "Page": "Home",
                    "_AvailableRoutes": [
                                        "http://127.0.0.1:5001/hybrid_recommendation?book_title=BookName", 
                                        "http://127.0.0.1:5001/content_recommendation?book_title=BookName", 
                                        "http://127.0.0.1:5001/collaborative_recommendation?book_title=BookName"
                                        ]
                    })

@app.route('/api/top_books', methods=['GET'])
def  top_books():
    return jsonify({"data": df_popularity.to_dict(orient="records")})

@app.route('/api/recommend', methods=['GET'])
def recommendation():
    book_title = request.args.get('book_title')
    recommendations = recommend(book_title)
    return jsonify(recommendations)

@app.route('/api/content_recommendation', methods=['GET'])
def  content_recommendation():
    book_title = request.args.get('book_title')
    recommendations = content_based_recommender(book_title, df_books)
    return jsonify(recommendations)

@app.route('/api/collaborative_recommendation', methods=['GET'])
def collaborative_recommendation():
    book_title = request.args.get('book_title')
    recommendations = recommend(book_title)
    return jsonify(recommendations)

@app.route('/api/hybrid_recommendation', methods=['GET'])
def hybrid_recommendation_route():
    book_title = request.args.get('book_title')
    recommendations = hybrid_recommendation(book_title)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

