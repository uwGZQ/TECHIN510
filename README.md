# TECHIN 510 Lab 3
Promptbase is a Streamlit application designed to manage and render prompt templates for ChatGPT, including functionalities for creating, reading, updating, deleting, searching, and sorting prompts. It also allows users to mark prompts as favorites and render prompts from templates into final forms.

## Configuration

Before running the application, you need to set up the required environment variables. These variables are necessary for database connections and potentially other configurations.

## Environment Variables
Create a `.env` file in the root directory of your project and add the following environment variables:

```bash
DATABASE_URL=postgres://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME
```

Replace `USERNAME`, `PASSWORD`, `HOST`, `PORT`, and `DATABASE_NAME` with your PostgreSQL database credentials.

## Running the Application

To run the application, you need to have installed the packages in `requirements.txt`
navigate to the project's root directory in your terminal and run the application with:
```bash
streamlit run app.py

```

## Features

* CRUD Operations: Create, read, update, and delete prompts.
* Search and Sort: Easily find prompts by search and organize them by creation date, update date, or title.
* Favorites: Mark prompts as favorites for quick access.
* Template Rendering: Render prompt templates into final forms by filling in placeholders.