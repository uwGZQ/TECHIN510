# AI Painter Helper

> Ziqi Gao, Chenxi Guo, Grace Rao

AI Painter Helper is a Streamlit web application that integrates with DALL-E models to generate and manage images based on textual prompts. It uses a PostgreSQL database for storage, and Supabase for image hosting. The application features capabilities such as image generation, search, caption creation, image update, and deletion.

## Features

* Generate Image: Users can enter a prompt to generate an image using the DALL-E model.
* Search Images: Allows users to search through generated images using keywords.
* Create Caption: Users can add captions to images by selecting from predefined prompts or writing their own.
* Update Image: Users can update existing images by providing a new prompt, which regenerates the image.
* Delete Image: This feature enables users to delete images from the database and storage.
* View All Images: Displays all images stored in the database along with their details and cost calculations.

## Technologies

Python: Primary programming language.
Streamlit: Framework for building and deploying the web app.
PostgreSQL: Database to store image details.
Supabase: Cloud service for image storage and retrieval.
DALL-E: OpenAI's model used for generating images from textual prompts.


## Problem to solve
The AI Painter Helper application addresses key challenges in digital content creation by simplifying the generation of custom images through AI-driven technology. It enhances user engagement by enabling dynamic image generation and captioning based on textual prompts, and streamlines image management with functionalities for searching, updating, and deleting images. This tool makes high-quality image creation accessible and cost-effective for users without advanced design skills, integrating seamlessly with databases and cloud storage to provide a comprehensive and user-friendly solution for content creators of all levels.

## Installation

1. Clone the Repository

```bash
git clone https://github.com/your-repository/ai-painter-helper.git
cd ai-painter-helper
```

2. Set Up a Virtual Environment (Optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Environment Variables
Set up the necessary environment variables or use a .env file:

```makefile
DATABASE_URL=your_database_url
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENAI_API_KEY=your_openai_api_key
```

5. Initialize the Database

Make sure PostgreSQL is running and accessible using DATABASE_URL.
Run the initialization commands in Python shell or script:

```python
from database import Database
db = Database(os.getenv("DATABASE_URL"))
db.create_table()
```

6. Run the Application

```bash
streamlit run app.py
```

## Usage

After launching the app, navigate through the sidebar to access different functionalities:

* Generate new images by entering prompts.
* Search, view, and manage existing images.
* Update or delete images as required.
* The application is designed to be intuitive and user-friendly, allowing seamless navigation and operation without requiring extensive technical knowledge.

## Reflections
### What I Learned
1.  Integration of Machine Learning Models: I gained hands-on experience integrating DALL-E, a sophisticated image generation model, into a web application. This deepened my understanding of how machine learning models can be applied in practical, user-facing applications.

2. Full Stack Development: The project provided a comprehensive overview of full-stack development practices. I worked with both the frontend (using Streamlit) and the backend (handling databases with PostgreSQL and image storage with Supabase), which enriched my skill set across the development spectrum.

3. Cloud Services: Utilizing Supabase for cloud-based image storage was a significant learning curve. It taught me about managing digital assets in the cloud and how to generate and handle secure, signed URLs for private access.

4. Performance Optimization: Implementing features like image caching and efficient database queries helped me understand the importance of backend optimization for improving the responsiveness and scalability of web applications.

### Challenges and Problems Faced

1. 2API Rate Limits: Handling OpenAI API rate limits was a challenge, especially when multiple users accessed the application simultaneously. This required implementing robust error handling and rate limit management.

2. Image Data Handling: Converting between different image formats and managing binary data streams was complex. Ensuring that images were correctly encoded and decoded when uploading to and retrieving from cloud storage required careful handling to prevent data corruption.

4. User Interface Design: Designing an intuitive user interface with Streamlit that could handle dynamic content updates (like image generation and deletion) was challenging. Streamlit's session state management was crucial for maintaining state across user interactions without reloading the entire page.

4. Security and Data Privacy: Ensuring that the application was secure, especially handling API keys and user-generated content, was paramount. Implementing environment variables and secure access mechanisms was a critical part of this process.