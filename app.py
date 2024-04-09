


import os
from dataclasses import dataclass, field

import streamlit as st
import psycopg2
from dotenv import load_dotenv
load_dotenv()
from urllib.parse import quote
raw_pass = os.getenv("SUPABASE_PASSWORD")
passwd = quote(raw_pass)

con = psycopg2.connect(f"postgres://postgres.ryuispstuutbtcbxjcma:{passwd}@aws-0-us-west-1.pooler.supabase.com:5432/postgres")
cur = con.cursor()



# Ensure the table exists and has all necessary columns
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS prompts (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        prompt TEXT NOT NULL,
        favorite BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
)
con.commit()  # Commit any changes made to the database

@dataclass
class Prompt:
    title: str
    prompt: str
    id: int = field(default=None)
    favorite: bool = field(default=False)

def prompt_form(prompt=Prompt("", "", None, False)):
    with st.form(key="prompt_form"):
        title = st.text_input("Title", value=prompt.title, max_chars=50)
        prompt_text = st.text_area("Prompt", height=200, value=prompt.prompt)
        favorite = st.checkbox("Favorite", value=prompt.favorite)
        submitted = st.form_submit_button("Submit")
        if submitted and title and prompt_text:  # Validation check
            return Prompt(title, prompt_text, prompt.id, favorite)

def update_prompt(id, title, prompt_text, favorite):
    cur.execute(
        "UPDATE prompts SET title = %s, prompt = %s, favorite = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
        (title, prompt_text, favorite, id,)
    )
    con.commit()

def insert_prompt(title, prompt_text, favorite):
    cur.execute(
        "INSERT INTO prompts (title, prompt, favorite) VALUES (%s, %s, %s) RETURNING id",
        (title, prompt_text, favorite,)
    )
    con.commit()
    return cur.fetchone()[0]

st.title("Promptbase")
st.subheader("A simple app to store and retrieve prompts")

# Search and Sorting UI
search_query = st.text_input('Search prompts')
sort_by_date = st.checkbox('Sort by date', value=True)
sort_order = "DESC" if sort_by_date else "ASC"
# Prepare query based on user input
search_condition = "WHERE title ILIKE %s OR prompt ILIKE %s" if search_query else ""
order_condition = f"ORDER BY created_at {sort_order}"
cur.execute(f"SELECT id, title, prompt, favorite FROM prompts {search_condition} {order_condition}", (f"%{search_query}%", f"%{search_query}%"))
prompts = [Prompt(title=row[1], prompt=row[2], id=row[0], favorite=row[3]) for row in cur.fetchall()]

# Display prompts with options to edit, delete, and mark as favorite
for prompt in prompts:
    with st.expander(prompt.title):
        st.code(prompt.prompt)
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            if st.button("Edit", key=f"edit_{prompt.id}"):
                edited_prompt = prompt_form(prompt)
                if edited_prompt:
                    update_prompt(edited_prompt.id, edited_prompt.title, edited_prompt.prompt, edited_prompt.favorite)
                    st.success("Prompt updated successfully!")
                    st.experimental_rerun()
        with col2:
            if st.button("Delete", key=f"delete_{prompt.id}"):
                cur.execute("DELETE FROM prompts WHERE id = %s", (prompt.id,))
                con.commit()
                st.success("Prompt deleted successfully!")
                st.experimental_rerun()
        with col3:
            if st.checkbox("Favorite", value=prompt.favorite, key=f"fav_{prompt.id}"):
                update_prompt(prompt.id, prompt.title, prompt.prompt, not prompt.favorite)

# Add new prompt form
new_prompt = prompt_form()
if new_prompt:
    insert_prompt(new_prompt.title, new_prompt.prompt, new_prompt.favorite)
    st.success("Prompt added successfully!")

# Ensure the connection is closed to prevent resource leaks
con.close()
