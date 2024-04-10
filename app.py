import os
import re
from dataclasses import dataclass, field
import streamlit as st
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

# Load environment variables and establish database connection
load_dotenv()
con = psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=DictCursor)
cur = con.cursor()

# Database setup
cur.execute("""
    CREATE TABLE IF NOT EXISTS prompts (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        prompt TEXT NOT NULL,
        is_favorite BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
con.commit()

@dataclass
class Prompt:
    id: int = field(default=None)
    title: str = field(default='')
    prompt: str = field(default='')
    is_favorite: bool = field(default=False)

def execute_sql(sql, params=None, commit=False):
    cur.execute(sql, params or ())
    if commit:
        con.commit()
    else:
        return cur.fetchall()

def add_or_update_prompt(prompt: Prompt):
    if prompt.id:
        execute_sql("UPDATE prompts SET title = %s, prompt = %s, is_favorite = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                    (prompt.title, prompt.prompt, prompt.is_favorite, prompt.id), commit=True)
    else:
        cur.execute("INSERT INTO prompts (title, prompt, is_favorite) VALUES (%s, %s, %s) RETURNING id",
                    (prompt.title, prompt.prompt, prompt.is_favorite))
        con.commit()
        prompt.id = cur.fetchone()[0]

def delete_prompt(prompt_id: int):
    execute_sql("DELETE FROM prompts WHERE id = %s", (prompt_id,), commit=True)

def get_prompts(search_query: str = "", only_favorites: bool = False, sort_by: str = "created_at"):
    base_query = "SELECT * FROM prompts WHERE (%s = '' OR title ILIKE %s OR prompt ILIKE %s)"
    if only_favorites:
        base_query += " AND is_favorite = TRUE"
    
    order_clause = " ORDER BY "
    if sort_by == "created_at":
        order_clause += "created_at DESC"
    elif sort_by == "updated_at":
        order_clause += "updated_at DESC"
    elif sort_by == "title":
        order_clause += "title ASC"

    final_query = base_query + order_clause
    return [Prompt(row['id'], row['title'], row['prompt'], row['is_favorite']) for row in execute_sql(final_query, [search_query, f"%{search_query}%", f"%{search_query}%"])]

def prompt_form(prompt=Prompt()):
    with st.form(key=f"prompt_{prompt.id or 'new'}"):
        title = st.text_input("Title", value=prompt.title)
        prompt_text = st.text_area("Prompt", height=300, value=prompt.prompt)
        is_favorite = st.checkbox("Favorite", value=prompt.is_favorite)
        submitted = st.form_submit_button("Submit")
        if submitted and title and prompt_text:
            return Prompt(prompt.id, title, prompt_text, is_favorite)

def render_template_prompt(prompt_id):
    prompt = next((p for p in get_prompts() if p.id == prompt_id), None)
    if prompt:
        placeholders = re.findall(r'\{(.+?)\}', prompt.prompt)
        user_values = {}
        for placeholder in placeholders:
            user_values[placeholder] = st.text_input(f"Value for {placeholder}", key=f"placeholder_{placeholder}")
        if st.button("Generate Prompt", key="generate_prompt"):
            final_prompt = prompt.prompt
            for placeholder, value in user_values.items():
                final_prompt = final_prompt.replace(f'{{{placeholder}}}', value)
            st.text_area("Your final prompt:", value=final_prompt, height=200, key="final_prompt")

def app():
    st.title("Promptbase")
    st.sidebar.subheader("Actions")
    if st.sidebar.button("Create New Prompt"):
        st.session_state['selected_prompt'] = Prompt()

    sort_by = st.sidebar.selectbox("Sort by", options=["created_at", "updated_at", "title"], index=0)
    search_query = st.sidebar.text_input("Search prompts")
    only_favorites = st.sidebar.checkbox("Show only favorites")
    selected_prompt = st.session_state.get('selected_prompt', None)

    if selected_prompt is not None:
        prompt = prompt_form(selected_prompt)
        if prompt:
            add_or_update_prompt(prompt)
            st.success("Prompt saved successfully!")
            del st.session_state['selected_prompt']

    prompts = get_prompts(search_query, only_favorites, sort_by)
    for prompt in prompts:
        with st.expander(f"{prompt.title}"):
            st.text(prompt.prompt)
            if st.button("Edit", key=f"edit_{prompt.id}"):
                st.session_state['selected_prompt'] = prompt
            if st.button("Delete", key=f"delete_{prompt.id}"):
                delete_prompt(prompt.id)
                st.experimental_rerun()
            if st.button("Toggle Favorite", key=f"fav_{prompt.id}"):
                prompt.is_favorite = not prompt.is_favorite
                add_or_update_prompt(prompt)
                st.experimental_rerun()

    st.sidebar.subheader("Render a Template")
    prompt_title_to_id = {prompt.title: prompt.id for prompt in prompts}
    selected_prompt_title = st.sidebar.selectbox("Choose a prompt to render", options=list(prompt_title_to_id.keys()))
    selected_prompt_id = prompt_title_to_id.get(selected_prompt_title)
    if selected_prompt_id:
        render_template_prompt(selected_prompt_id)
    # prompt_ids = [prompt.id for prompt in get_prompts()]
    # selected_prompt_id = st.sidebar.selectbox("Choose a prompt to render", options=prompt_ids, index=0)
    # if selected_prompt_id:
    #     render_template_prompt(selected_prompt_id)

if __name__ == "__main__":
    app()
