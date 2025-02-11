# Vehicles_info
 Project Description
This interactive dashboard allows users to explore a car listings dataset with insights into various attributes like car prices, mileage (odometer), fuel type, and car manufacturer. Built using Streamlit for interactivity and Plotly for visualizations, the dashboard provides an easy-to-use interface for users to filter data, analyze trends, and visualize insights about the car listings.

Technologies Used
Streamlit: For creating interactive web apps.
Plotly Express: For creating interactive visualizations.
Pandas: For data manipulation and analysis.
Python: The core programming language.

Dataset Overview
The dataset used for this project contains car listings with columns such as:

Model Year: The year of manufacture of the car.
Price: The asking price for the car.
Odometer: The mileage of the car (in kilometers or miles).
Fuel Type: The type of fuel the car uses (e.g., Gas, Electric, Hybrid).
Manufacturer: The car's brand or manufacturer.

Key Preprocessing Steps:
Missing Values:
Filled missing values in paint_color with "No info!".
Filled missing numerical values with 0.
Data Type Conversion:
Changed columns like model_year, cylinders, and is_4wd to integers.
Converted date_posted to a datetime object.
Changed odometer to integers.
Data Cleaning:
Removed any duplicates from the dataset.
Added a new column manufacturer by extracting the car brand from the model name.
Created a new column h_l_mileage to categorize cars into Above 100k or Lower than 100k mileage groups.

render URL : https://vehicles-info-version-2.onrender.com
