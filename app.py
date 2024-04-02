# app.py
import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    """Loads the Iris dataset."""
    data = sns.load_dataset('iris')
    return data

def display_header(app_title):
    """Displays the application title and introduction."""
    st.title(app_title)
    st.write("""
    This Streamlit web app demonstrates data analysis and visualization of the Iris dataset. 
    The Iris dataset is a classic dataset in the fields of machine learning and statistics 
    and includes measurements of 150 iris flowers from three different species.
    """)

def user_input_features(iris):
    """Generates user input features for filtering the dataset."""
    species = st.sidebar.selectbox('Species', options=iris['species'].unique(), index=0)
    petal_length_min, petal_length_max = iris['petal_length'].min(), iris['petal_length'].max()
    petal_length = st.sidebar.slider('Petal Length', 
                                     float(petal_length_min), 
                                     float(petal_length_max), 
                                     (float(petal_length_min), float(petal_length_max)))
    return species, petal_length

def filter_data(iris, species, petal_length):
    """Filters the dataset based on user selection."""
    filtered_data = iris[(iris['species'] == species) & 
                         (iris['petal_length'] >= petal_length[0]) & 
                         (iris['petal_length'] <= petal_length[1])]
    return filtered_data

def display_data(data):
    """Displays the filtered dataset."""
    st.write("## Filtered Data", data)
    

def plot_data(data):
    """Plots the filtered dataset."""
    fig, ax = plt.subplots()
    sns.scatterplot(data=data, x='sepal_length', y='sepal_width', hue='species', style='species', ax=ax)
    plt.title('Sepal Length vs. Sepal Width')
    st.pyplot(fig)

# Load the dataset
iris = load_data()

# Display the header
display_header("Iris Dataset Analysis")

# User input for filtering
species_selected, petal_length_selected = user_input_features(iris)

# Filter the data based on user input
filtered_iris = filter_data(iris, species_selected, petal_length_selected)

# Display the filtered data
display_data(filtered_iris)

# Visualize the filtered data
plot_data(filtered_iris)
