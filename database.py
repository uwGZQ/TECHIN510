import time
import os
import psycopg2
from supabase import create_client
from PIL import Image
# import supabase
from datetime import datetime
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()
# Supabase settings
DATABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
bucket_name = 'TECHIN510'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class Database:
    def __init__(self, database_url) -> None:
        self.database_url = database_url
        print(f"Connecting to database: {self.database_url}")
        self.connect()

    def connect(self):
        retries = 5
        while retries > 0:
            try:
                self.con = psycopg2.connect(self.database_url)
                self.cur = self.con.cursor()
                return
            except psycopg2.OperationalError as e:
                print(f"Connection failed: {e}")
                retries -= 1
                time.sleep(5)
        raise Exception("Could not connect to the database after several retries")

    def check_connection(self):
        try:
            self.cur.execute("SELECT 1")
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            print("Connection lost, reconnecting...")
            self.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def create_table(self):
        self.check_connection()
        q = """
        CREATE TABLE IF NOT EXISTS dall_e_images (
            id SERIAL PRIMARY KEY,
            prompt TEXT NOT NULL,
            image_name TEXT NOT NULL,
            caption TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            modified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.cur.execute(q)
        self.con.commit()
            
    def drop_table(self):
        self.check_connection()
        q = "DROP TABLE IF EXISTS dall_e_images;"
        self.cur.execute(q)
        self.con.commit()
        

    def add_column(self, c_name, c_type):
        self.check_connection()
        q = """
        ALTER TABLE dall_e_images
        ADD COLUMN IF NOT EXISTS %s %s;
        """
        self.cur.execute(q, (c_name, c_type))
        self.con.commit()
        
    def print_table(self):
        self.check_connection()
        q = """
        SELECT * FROM dall_e_images;
        """
        self.cur.execute(q)
        rows = self.cur.fetchall()
        for row in rows:
            print(row)


    # upload
    def _upload_image_to_storage(self, image_input, bucket_name, image_name):
        import io
        import numpy as np
        import torch
        from PIL import Image
        if isinstance(image_input, Image.Image):
            image = image_input
        elif isinstance(image_input, np.ndarray):
            if image_input.ndim == 2:  # greyscale
                image = Image.fromarray(image_input, 'L')
            elif image_input.ndim == 3:
                if image_input.shape[2] == 3:  # RGB
                    image = Image.fromarray(image_input, 'RGB')
                elif image_input.shape[2] == 4:  # RGBA
                    image = Image.fromarray(image_input, 'RGBA')
                else:
                    raise ValueError("Unsupported numpy array shape")
            else:
                raise ValueError("Unsupported numpy array shape")
        elif isinstance(image_input, torch.Tensor):
            if image_input.ndim == 2:  # greyscale
                image = Image.fromarray(image_input.numpy(), 'L')
            elif image_input.ndim == 3:
                if image_input.shape[0] == 3:  # CxHxW, RGB
                    image = Image.fromarray(image_input.permute(1, 2, 0).numpy(), 'RGB')
                elif image_input.shape[0] == 4:  # CxHxW, RGBA
                    image = Image.fromarray(image_input.permute(1, 2, 0).numpy(), 'RGBA')
                else:
                    raise ValueError("Unsupported tensor shape")
            else:
                raise ValueError("Unsupported tensor shape")
        else:
            raise TypeError("Unsupported input type")

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        res = supabase.storage.from_(bucket_name).upload(file=img_byte_arr, path=image_name, file_options={"content-type": "image/png"})
        return res



    def save_image(self, prompt, image, bucket_name):
        self.check_connection()
        q = """
        INSERT INTO dall_e_images (prompt, image_name, created_at, modified_at)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """
        image_name = f"{prompt.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        
        res = self._upload_image_to_storage(image, bucket_name, image_name)
        if res.status_code != 200:
            return {'error': {'message': res.text}}
        else:    
            self.cur.execute(q, (prompt, image_name, datetime.now(), datetime.now()))
            self.con.commit()
            return self.cur.fetchone()[0]
    
    
    def search_image(self, prompt):
        # search images based on a prompt and get the image from the bucket
        self.check_connection()
        print(prompt)
        q = """
        SELECT * FROM dall_e_images WHERE prompt ILIKE %s;
        """
        self.cur.execute(q, (f'%{prompt}%',))
        rows = self.cur.fetchall()
        images = []
        for row in rows:
            image_id, prompt, image_name, caption, created_at, modified_at = row
            response = supabase.storage.from_(bucket_name).create_signed_url(image_name, expires_in=60*60*24)
            images.append((image_id, prompt, image_name, caption, created_at, modified_at, response['signedURL']))
        return images
    
    def search_image_by_name(self, image_name):
        self.check_connection()
        q = """
        SELECT * FROM dall_e_images WHERE image_name = %s;
        """
        self.cur.execute(q, (image_name,))
        row = self.cur.fetchone()
        if row:
            image_id, prompt, image_name, caption, created_at, modified_at = row
            response = supabase.storage.from_(bucket_name).create_signed_url(image_name, expires_in=60*60*24)
            return (image_id, prompt, image_name, caption, created_at, modified_at, response['signedURL'])
        return None
    
    def search_all_images(self):
        self.check_connection()
        q = """
        SELECT * FROM dall_e_images;
        """
        # return id prompt image_name caption created_at modified_at url
        self.cur.execute(q)
        rows = self.cur.fetchall()
        images = []
        for row in rows:
            image_id, prompt, image_name, caption, created_at, modified_at = row
            response = supabase.storage.from_(bucket_name).create_signed_url(image_name, expires_in=60*60*24)
            
            images.append((image_id, prompt, image_name, caption, created_at, modified_at, response['signedURL']))
        return images

    

    # delete
    def delete_image(self, image_name):
        self.check_connection()
        q = """
        DELETE FROM dall_e_images WHERE image_name = %s RETURNING image_name;
        """
        self.cur.execute(q, (image_name,))
        image_name = self.cur.fetchone()[0]
        self.con.commit()
        res = self._delete_image_from_bucket(image_name)
        return image_name

    def _delete_image_from_bucket(self, image_name):
        retries = 5
        while retries > 0:
            try:
                response = supabase.storage.from_(bucket_name).remove([image_name])
                if response.status_code == 200:
                    return {'message': 'Image deleted successfully from bucket'}
            except Exception as e:
                retries -= 1
                if retries == 0:
                    return {'error': {'message': str(e)}}

    def add_caption_to_image(self, image_name, caption):
        self.check_connection()
        q = """
        UPDATE dall_e_images SET caption = %s, modified_at = %s WHERE image_name = %s;
        """
        self.cur.execute(q, (caption, datetime.now(), image_name))
        self.con.commit()
        
    def renew_prompt_and_image(self, image_name, new_prompt, new_image):
        self.check_connection()
        new_image_name = f"{new_prompt.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        q = """
        UPDATE dall_e_images SET prompt = %s, image_name = %s, modified_at = %s WHERE image_name = %s;
        """
        self.cur.execute(q, (new_prompt, new_image_name, datetime.now(), image_name))
        self.con.commit()
        self._delete_image_from_bucket(image_name)
        self._upload_image_to_storage(new_image, bucket_name, new_image_name)
        






if __name__ == "__main__":
    db = Database(DATABASE_URL)
    db.print_table()
    