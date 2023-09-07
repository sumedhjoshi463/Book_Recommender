import uvicorn 
from fastapi import FastAPI

import numpy as np 
import pickle

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = FastAPI()

@app.get('/')
def index():
    return {'Welcome to Book recommender System'}



@app.get('/top_books')
def top_books():
    return {'book-title': popular_df['Book-Title'][0], 'author': popular_df['Book-Author'][0], 'votes':popular_df['num_votes'][0], 'ratings': popular_df['num_ratings'][0]}



@app.get('/recommed_books')
def recommed_books(book_name):
    index = np.where(pt.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    
    return data

    if __name__ == '__main__':
        uvicorn.run(app, host='127.0.0.1',port=8000)