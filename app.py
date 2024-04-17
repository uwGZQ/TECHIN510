import streamlit as st
from books_scraper import scrape_books_from_page
from db import Database
import requests
from dotenv import load_dotenv
import os
import pandas as pd
load_dotenv()

# Initialize the database
db = Database(os.getenv("DB_NAME"), os.getenv("DB_USER"), os.getenv("DB_PASSWD"), os.getenv("DB_HOST"))

def setup_database():
    """ Create the table and insert scraped data into the database """
    db.create_table()
    base_url = 'http://books.toscrape.com/catalogue/category/books_1/page-{}.html'
    
    for page in range(1, 51):  
        books = []
        response = requests.get(base_url.format(page))
        books = scrape_books_from_page(response.text)
        for book in books:
            db.add_book(book['title'], book['price'], book['rating'], book['description'], book['url'])

def display_books():
    with db.connect() as cur:
        cur.execute("SELECT * FROM bookstore")
        books = cur.fetchall()
        return pd.DataFrame(books, columns=["id", "title", "price", "rating", "description", "url","created_at","updated_at"])

def fetch_books(search_query, search_type, sort_order):
    if search_type == 'title':
        query = f"SELECT * FROM bookstore WHERE title ILIKE %s ORDER BY {sort_order};"
    elif search_type == 'description':
        query = f"SELECT * FROM bookstore WHERE description ILIKE %s ORDER BY {sort_order};"
    
    db.cur.execute(query, ('%' + search_query + '%',))
    return db.cur.fetchall()

def main():
    st.title("Book Search and Filter App")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Setup Database"):
            setup_database()
            st.success("Database setup complete!")

    with col2:
        show_books = st.button("Display Books")

    if show_books:
        df = display_books()
        if not df.empty:
            st.dataframe(df)
        else:
            st.write("No books found.")
        
    search_query = st.text_input("Search for bookstore")
    search_type = st.selectbox("Search by", ('title', 'description'))
    sort_order = st.selectbox("Sort by", ('rating ASC', 'rating DESC', 'price ASC', 'price DESC'))

    if st.button("Search"):
        if search_query:
            results = fetch_books(search_query, search_type, sort_order)
            if results:
                st.dataframe(pd.DataFrame(results, columns=["id", "title", "price", "rating", "description", "url","created_at","updated_at"]))
                for book in results:
                    st.text(f"Title: {book[1]}, Price: {book[2]}, Rating: {book[3]}, Description: {book[4]}")
            else:
                st.text("No books found matching the criteria.")
        else:
            st.text("Please enter a search term.")


if __name__ == "__main__":
    main()
