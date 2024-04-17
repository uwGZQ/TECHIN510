# TECHIN 510 Lab 4
This Streamlit application allows users to interact with a database of books. It provides functionalities for setting up the database, loading book data, and enabling users to search and filter books based on various criteria such as title, description, price, and rating.

## Features

- **Setup Database**: Initialize the database and create necessary tables.
- **Display Books**: View all books in the database.
- **Search and Filter**: Search books by title or description and filter them by rating or price.

## Requirements
See `requirements.txt`.
**Install dependencies**:
```bash
pip install -r requirements.txt
```



## Setup

Before running the application, ensure that your PostgreSQL database is configured:

1. Update the database connection details in `db.py` with your PostgreSQL credentials:
```python
db = Database('your_dbname', 'your_username', 'your_password', 'localhost')
```
2. Ensure the PostgreSQL server is running.

## Running the App

To run the app, execute the following command from the terminal within the project directory:

```bash
streamlit run app.py
```