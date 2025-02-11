import pandas as pd 
import plotly.express as px
import streamlit as st 
vehicles_info = pd.read_csv('vehicles_us.csv')

for model in vehicles_info['model'].unique():
    # find the median for each of these models
    median_value = vehicles_info[vehicles_info['model'] == model]['cylinders'].median()
    
    # find the rows with these models and use a simple fillna
    vehicles_info.loc[vehicles_info['model']==model, 'cylinders'] = vehicles_info.loc[vehicles_info['model']==model, 'cylinders'].fillna(median_value)    
vehicles_info['price'] = pd.to_numeric(vehicles_info['price'], errors='coerce')

# Fill any NaN values in 'price' column with 0 (or use another placeholder)
vehicles_info['price'] = vehicles_info['price'].fillna(0)
#Checking for missing and fill it 
print(vehicles_info.isna().sum())
#Filling all the missing in vehicle_info DataFrame with 'No info!' in 'paint_color'.
vehicles_info['paint_color'] = vehicles_info['paint_color'].fillna('No info!')
#filling all numerical missing with 0 
vehicles_info = vehicles_info.fillna(0)
#Checking for duplicates in vehicle_info.
print(vehicles_info.duplicated().sum())
#We have ZERO duplicate in the DataFrame

#Switching 'model_year' and 'cylinders' and 'is_4wd'Dtype from object and float to int
vehicles_info[['model_year', 'cylinders', 'is_4wd']] = vehicles_info[['model_year', 'cylinders', 'is_4wd']].astype(int)
#switching 'date_posted' Dtype from object to DateTime
vehicles_info['date_posted'] = pd.to_datetime(vehicles_info['date_posted'])
#switching 'odometer' Dtype from float to int
vehicles_info['odometer'] = vehicles_info['odometer'].astype(int)
#Adding a new column to the dataframe we will call it manufacturer
manufacturers = ['bmw', 'ford', 'chrysler', 'nissan', 'dodge', 'chevrolet', 
                 'toyota', 'honda', 'jeep', 'hyundai', 'gmc', 'kia', 
                 'subaru', 'volkswagen', 'mercedes', 'ram', 'cadillac', 'acura', 'buick']

# Function to extract manufacturer
def extract_manufacturer(model_name):
    model_name_clean = model_name.strip().lower()  # Clean the model name
    for brand in manufacturers:
        if brand in model_name_clean:  
            return brand  # Return the first matching brand
    return 'No info!'  # If no brand is found

# Apply function and create the new column
vehicles_info['manufacturer'] = vehicles_info['model'].apply(extract_manufacturer)
#adding a column for high and low milage.
vehicles_info['h_l_mileage'] = ''
def high_low(odometer):
    if odometer >= 100000:
        return 'Above 100k'
    elif odometer < 100000:
        return 'Lower than 100k'
    

# Apply the function to the 'odometer' column
vehicles_info['h_l_mileage'] = vehicles_info['odometer'].apply(high_low)
#counting how many cars we do have from the same model
models_per_year = vehicles_info[['model_year', 'model']].groupby('model').count().reset_index()
#filtering vehicle_info years from 1950 till 2020
start_year = 1950
end_year = 2020
filtered_data = vehicles_info[(vehicles_info['model_year'] >= start_year) & (vehicles_info['model_year'] <= 2020)]
#Histogram plot for odometers higher than a 100k and lower than 100k per year model.
high_low_per_year = filtered_data.groupby(['model_year', 'h_l_mileage'])['model'].count().reset_index()
st.header('Car advertisment Dataset')
st.write(vehicles_info)

#hist for model year vs odometer 
st.title("Vehicle Mileage Distribution: Model Year vs. Odometer")
year_range = st.selectbox('SELECT YEAR:', options=sorted(vehicles_info['model_year'].unique(), reverse=True))
odometer_range = st.slider('SELECT MILEAGE RANGE:', 
                           min_value=int(vehicles_info['odometer'].min()), 
                           max_value=int(vehicles_info['odometer'].max()), 
                           value=(int(vehicles_info['odometer'].min()), int(vehicles_info['odometer'].max())))
col = st.color_picker('SELECT PLOT COLOR', '#636EFA')
# Filter Data Based on User Selection
filtered_df = vehicles_info[(vehicles_info['model_year'] == year_range) & 
                            (vehicles_info['odometer'].between(odometer_range[0], odometer_range[1]))]

# Create Histogram
plot = px.histogram(filtered_df, x="odometer", nbins=30, color_discrete_sequence=[col],
                    title=f"Odometer Distribution for {year_range}",
                    labels={"odometer": "Odometer (Mileage)"})

# Display Plot
st.plotly_chart(plot)

st.title("Car Price Distribution by Model Year")
st.subheader("Analyze how car prices vary across different model years")

# Select Year (Descending Order)
year_selected = st.selectbox('SELECT MODEL YEAR:', options=sorted(vehicles_info['model_year'].unique(), reverse=True))

# Select Color
color_choice = st.color_picker('SELECT PLOT COLOR', '#FF5733')

# Filter Data Based on Selected Year
filtered_data = vehicles_info[vehicles_info['model_year'] == year_selected]

# Create Histogram for Price Distribution
fig = px.histogram(filtered_data, x="price", nbins=50, color_discrete_sequence=[color_choice],
                   title=f"Price Distribution for {year_selected} Model Year",
                   labels={"price": "Price ($)"})
fig.update_layout(
    xaxis_title_text='Price ($)',
    yaxis_title_text='Number of cars'
)
# Display Plot
st.plotly_chart(fig)

st.title("Car Listings Count by Manufacturer")
st.subheader("See which car brands have the most listings in the dataset")

# Select Color
color_choice = st.color_picker('SELECT BAR COLOR', '#3498db')

# Count listings per manufacturer
manufacturer_counts = vehicles_info['manufacturer'].value_counts().reset_index()
manufacturer_counts.columns = ['manufacturer', 'count']

# Create Bar Chart
manufacturer_counts_bar = px.bar(manufacturer_counts, x='manufacturer', y='count', color_discrete_sequence=[color_choice],
             title="Number of Listings by Car Manufacturer",
             labels={'manufacturer': 'Car Manufacturer', 'count': 'Number of Listings'})

# Display Plot
st.plotly_chart(manufacturer_counts_bar)


st.title("Car Price Distribution by Fuel Type")
st.subheader("Explore how car prices vary by fuel type")

# Checkbox to show all fuel types or filter by one
show_fuel_type_filter = st.checkbox("Filter by Fuel Type")

# Select Fuel Type if checkbox is selected
fuel_types = vehicles_info['fuel'].unique()
fuel_type_selected = st.selectbox("Select Fuel Type", options=fuel_types) if show_fuel_type_filter else None

# Select Color for the plot
color_choice = st.color_picker('SELECT PLOT COLOR', '#3498db')

# Filter data based on fuel type if checkbox is checked
if show_fuel_type_filter:
    filtered_data = vehicles_info[vehicles_info['fuel'] == fuel_type_selected]
    title = f"Price Distribution for {fuel_type_selected} Cars"
else:
    filtered_data = vehicles_info
    title = "Price Distribution for All Fuel Types"

# Create Histogram for Price Distribution
fuel_types_hist = px.histogram(filtered_data, x="price", y='fuel', color="fuel", nbins=30, color_discrete_sequence=[color_choice],
                   title=title, labels={"price": "Price ($)", "fuel": "Fuel Type"})

# Display Plot
st.plotly_chart(fuel_types_hist)
