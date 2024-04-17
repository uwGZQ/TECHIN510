import psycopg2
from datetime import datetime
from contextlib import contextmanager

class Database:
    def __init__(self, db_name, user, password, host='localhost') -> None:
        self.con = psycopg2.connect(
            dbname=db_name, user=user, password=password, host=host
        )
        self.cur = self.con.cursor()
        self.config = {
            'dbname': db_name,
            'user': user,
            'password': password,
            'host': host
        }

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS bookstore (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            price DECIMAL NOT NULL,
            rating INTEGER NOT NULL,
            description TEXT NOT NULL,
            url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(title),
            UNIQUE(url)
        );
        """
        self.cur.execute(query)
        self.con.commit()

    def add_book(self, title, price, rating, description, url):
        query = """
        INSERT INTO bookstore (title, price, rating, description, url)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (title) DO UPDATE SET
            title = EXCLUDED.title,
            price = EXCLUDED.price,
            rating = EXCLUDED.rating,
            description = EXCLUDED.description,
            updated_at = CURRENT_TIMESTAMP
        RETURNING id;
        """
        self.cur.execute(query, (title, price, rating, description, url))
        self.con.commit()
        return self.cur.fetchone()[0]

    def update_book(self, book_id, title=None, price=None, rating=None, description=None, url=None):
        query = []
        params = []

        if title:
            query.append("title = %s")
            params.append(title)
        if price:
            query.append("price = %s")
            params.append(price)
        if rating:
            query.append("rating = %s")
            params.append(rating)
        if description:
            query.append("description = %s")
            params.append(description)
        if url:
            query.append("url = %s")
            params.append(url)

        params.append(datetime.now())  
        params.append(book_id)

        if query:
            sql_update_query = f"UPDATE bookstore SET {', '.join(query)}, updated_at = %s WHERE id = %s;"
            self.cur.execute(sql_update_query, tuple(params))
            self.con.commit()

    def delete_book(self, book_id):
        query = "DELETE FROM bookstore WHERE id = %s;"
        self.cur.execute(query, (book_id,))
        self.con.commit()

    def get_book(self, book_id):
        query = "SELECT * FROM bookstore WHERE id = %s;"
        self.cur.execute(query, (book_id,))
        return self.cur.fetchone()

    def get_all_books(self):
        query = "SELECT * FROM bookstore;"
        self.cur.execute(query)
        return self.cur.fetchall()
    @contextmanager
    def connect(self):
        con = psycopg2.connect(**self.config)
        cur = con.cursor()
        try:
            yield cur
            con.commit()
        except Exception as e:
            con.rollback()
            raise
        finally:
            cur.close()
            con.close()
    def close(self):
        self.cur.close()
        self.con.close()
