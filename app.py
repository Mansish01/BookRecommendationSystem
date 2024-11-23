import pickle
import streamlit as st
import numpy as np

st.header("Book Recommendation system by Manish Gyawali")
model = pickle.load(open('artifacts/model.pkl', 'rb'))
books_name  = pickle.load(open('artifacts/books_name.pkl', 'rb'))
final_ratings  = pickle.load(open('artifacts/final_ratings.pkl', 'rb'))
table_pivot = pickle.load(open('artifacts/table_pivot.pkl', 'rb'))


selected_books = st.selectbox(
    "Type or select a book", 
    books_name
)

def recommended_books(book_name):
    books_list = []
    book_index = np.where(table_pivot.index == book_name)[0][0]
    distance, suggestions = model.kneighbors(table_pivot.iloc[book_index, :].values.reshape(1,-1), n_neighbors=6)

    poster_url = fetch_poster(suggestions)

    #because of the 2 dimensional array we are iterating again 
    for i in range(len(suggestions)):
        book= table_pivot.index[suggestions[i]]
        for j in book:
            books_list.append(j)

    return books_list, poster_url


def fetch_poster(suggestions):
    poster_url =  []
    book_name =  []
    ids_index = []

    for book_id in suggestions:
        book_name.append(table_pivot.index[book_id])
    
    for name in book_name[0]:
        index = np.where(final_ratings['Book-Title'] == name)[0][0]
        ids_index.append(index)

    for index in ids_index:
        url = final_ratings.iloc[index]['Image-URL-L']
        poster_url.append(url)

    return poster_url




if st.button('Search'):
    recommend_books, poster_url = recommended_books(selected_books)
    col1 , col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommend_books[1])
        st.image(poster_url[1])

    with col2:
        st.text(recommend_books[2])
        st.image(poster_url[2])


    with col3:
        st.text(recommend_books[3])
        st.image(poster_url[3])
        
    with col4:
        st.text(recommend_books[4])
        st.image(poster_url[4])

    with col5:
        st.text(recommend_books[5])
        st.image(poster_url[5])
