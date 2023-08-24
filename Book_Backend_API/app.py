from fastapi import FastAPI, Request, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from newapp import *

app = FastAPI()

# Enable CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Routes

@app.get("/")
def main_home():
    return {"message": "Welcome"}

@app.get("/api")
def home():
    return {
        "Page": "Home",
        "_AvailableRoutes": {
            "hybrid_recommendation": "/hybrid_recommendation?book_title=BookName",
            "content_recommendation": "/content_recommendation?book_title=BookName",
            "collaborative_recommendation": "/collaborative_recommendation?book_title=BookName",
        },
    }

@app.get("/api/top_books")
def top_books():
    return {"data": df_popularity.to_dict(orient="records")}

@app.get("/api/recommend")
def recommendation(book_title: str = Query(..., description="Title of the book")):
    recommendations = recommend(book_title)
    return recommendations

@app.get("/api/content_recommendation")
def content_recommendation(book_title: str = Query(..., description="Title of the book")):
    recommendations = content_based_recommender(book_title, df_books)
    return recommendations

@app.get("/api/collaborative_recommendation")
def collaborative_recommendation(book_title: str = Query(..., description="Title of the book")):
    recommendations = recommend(book_title)
    return recommendations

@app.get("/api/hybrid_recommendation")
def hybrid_recommendation_route(book_title: str = Query(..., description="Title of the book")):
    recommendations = hybrid_recommendation(book_title)
    return recommendations
