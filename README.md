# TECHIN 510 Lab 2

A data analysis website and a timer website for TECHIN 510 Lab 2.

## How to Run

Open the terminal and run the following commands:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run [app/timer].py
```

## What's Included

- `app.py`: The data analysis and visualization application
- `timer.py`: The timer application

## How to Use
This application offers two main functionalities, each accessible from the sidebar navigation:

### Data Analysis and Visualization (app.py)

- **Introduction**: The application also features an analysis and visualization of the Iris dataset, showcasing the power of Streamlit in handling data science projects.
- **Select Features**: Use the sidebar widgets to filter the Iris dataset based on species and petal length.
- **View Data**: The filtered dataset will be displayed on the main page.
- **Visualization**: A scatter plot of sepal length vs. sepal width for the filtered dataset will also be shown, providing insights into the data distribution among different Iris species.



### timer.app
#### World Clocks

- **Navigation**: Select the 'World Clocks' option from the sidebar.
- **Select Cities**: Choose one or multiple cities from the dropdown menu to view their current time.
- **UNIX Timestamp**: Optionally, you can display the current UNIX timestamp by checking the corresponding box.
- **Live Update**: The clocks update every second to reflect the current time in the selected cities.

#### UNIX Timestamp Conversion

- **Navigation**: Select the 'UNIX Timestamp Conversion' option from the sidebar.
- **Convert Timestamp**: Enter a UNIX timestamp into the input box. The application will display the corresponding human-readable date and time.

