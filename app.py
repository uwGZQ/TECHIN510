import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import datetime
import openai
import torch
from text2img import DALLEModel
from database import Database
import os
from supabase import create_client


DATABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
openai_key = os.getenv("OPENAI_API_KEY")
bucket_name = 'TECHIN510'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

db = Database(DATABASE_URL)
dalle_model = DALLEModel(
    ckpt= {"imagecap_model":"gpt-4o","txt2img_model":"dall-e-3","api-key":openai_key,"quality":"standard","size":"1024x1024"}, 
    precision = torch.float16, 
    device = torch.device("cuda")
)



# Streamlit app
st.set_page_config(page_title="AI Painter Helper", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Generate Image", "Search Images", "Create Caption", "Update Image", "Delete Image", "All Images"])

import streamlit as st
from datetime import datetime



def display_images(images, delete_mode = False):
    cols = st.columns(4) 
    for idx, img in enumerate(images):
        with cols[idx % 4]:
            st.image(img[6], caption=img[2], use_column_width=True)
            if delete_mode:
                if st.button("Delete", key = f"delete_{img[2]}"):
                    db.delete_image(img[2])
                    st.write(f"Image {img[2]} deleted.")
                    st.experimental_rerun()
            else:
                expander = st.expander("View Details", expanded=False)
                with expander:
                    st.text_area("Prompt", img[1], height=25, key = datetime.now(), disabled=True)
                    st.text_area("Caption", img[3], height=50, key = datetime.now(), disabled=True)
                    st.write(f"Created at: {img[4].strftime('%Y.%m.%d %H:%M:%S')}")
                    st.write(f"Modified at: {img[5].strftime('%Y.%m.%d %H:%M:%S')}")


if "price" not in st.session_state:
    st.session_state.price = 0



if page == "Generate Image":
    st.title("Generate Image")
    prompt = st.text_input("Enter prompt:")
    if st.button("Generate"):
        st.write("Generating image...")
        image = dalle_model.text2img(prompt)
        st.write("Image generated.")
        st.session_state.price += dalle_model.get_cost()
        st.image(image, caption=prompt)
        db.save_image(prompt, image, 'TECHIN510')

elif page == "Search Images":
    st.title("Search Images")
    prompt = st.text_input("Enter keyword:")
    if st.button("Search"):
        images = db.search_image(prompt)
        if images:
            display_images(images)
        else:
            st.write("No images found.")

elif page == "Create Caption":
    st.title("Create Caption")
    custom_prompt = ["Directly describe with brevity and as brief as possible the scene or characters without any introductory phrase like 'This image shows', 'In the scene', 'This image depicts' or similar phrases. Just start describing the scene please. Do not end the caption with a '.'. Some characters may be animated, refer to them as regular humans and not animated humans. Please make no reference to any particular style or characters from any TV show or Movie. Good examples: a cat on a windowsill, a photo of smiling cactus in an office, a man and baby sitting by a window, a photo of wheel on a car,",
                     "Describe the image as if you were explaining it to a blind person. Do not include any unnecessary details. Good examples: a photo of a cat sitting on a windowsill, a photo of a smiling cactus in an office",
                     "Describe the image as detailed as possible. Good examples: a cat sitting on a windowsill, a photo of a smiling cactus in an office",
                     "Write a story based on this image. What is happening in this image? What are the characters doing? What is the setting? What is the mood? What is the story behind this image?",
                     "Write the prompt by myself"]
    
    
    images = db.search_all_images()
    display_images(images)
    image_name = st.selectbox("Select image name:", [img[2] for img in images])
    choice = st.selectbox("Select caption prompt:", custom_prompt)
    if choice == "Write the prompt by myself":
        caption_prompt = st.text_input("Enter caption prompt:")
    else:
        caption_prompt = choice
    if st.button("Generate Caption"):
        image_searched = db.search_image_by_name(image_name)
        # (image_id, prompt, image_name, caption, created_at, modified_at, response['signedURL'])
        image_url = image_searched[6]
        st.write("Captioning image...")
        caption = dalle_model.image_caption(image_url, caption_prompt)
        db.add_caption_to_image(image_name, caption)
        st.write(f"Caption added: {caption}")
        st.experimental_rerun()

elif page == "Update Image":
    st.title("Update Image")
    images = db.search_all_images()
    display_images(images)
    image_name = st.selectbox("Select image name:", [img[2] for img in images])
    new_prompt = st.text_input("Enter new prompt:")
    if st.button("Update Image"):
        new_image = dalle_model.text2img(new_prompt)
        db.renew_prompt_and_image(image_name, new_prompt, new_image)
        st.image(new_image, caption=new_prompt)

elif page == "Delete Image":
    st.title("Delete Image")
    images = db.search_all_images()
    display_images(images, delete_mode = True)


elif page == "All Images":
    st.title("All Images")
    st.write("Current Cost of Images in This Session: $", st.session_state.price)
    images = db.search_all_images()
    display_images(images)
