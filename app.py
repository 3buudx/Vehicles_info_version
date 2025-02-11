import pandas as pd 
import plotly.express as px
import streamlit as st 
vehicles_info = pd.read_csv('vehicles_us.csv')
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
#models_per_year_scatter = px.scatter(models_per_year,
 #                                    x='model_year',
  #                                   y='model',
   #                                  title='Total cars from the same model',
    #                                 labels= dict(model = 'Car Model', model_year = 'Total cars'),
     #                                color='model',
      #                               color_discrete_sequence= px.colors.qualitative.Light24)
#Updating the size for fonts 
#models_per_year_scatter.update_layout(
 #   yaxis=dict(
  #      tickfont=dict(size=10),  # Adjust font size for better readability
   #     automargin=True,         # Prevent label cut-off
    #    title_standoff=15,       # Space between title and labels
     #   fixedrange=False         # Allow scrolling
    #),
    #xaxis=dict(
     #   tickfont=dict(size=14),
      #  range=[1990, 2025]  # Adjust based on your dataset
  #  )#,
   # hovermode="closest"
#)
# Enable scrolling by setting a fixed height
#models_per_year_scatter.update_layout(height=600)
#updating the range axis for X
#models_per_year_scatter.update_xaxes(range=[25, 3000])
#showing plot
#models_per_year_scatter.show(config={'responsive': False})
#st.plotly_chart(models_per_year_scatter, use_container_width=True)


#total of cars from the same manufacturer
cars_per_manufacturer = (
    vehicles_info.groupby(['manufacturer'])['model']
    .count()
    .reset_index()
    .rename(columns={'model': 'count'})
)
# Create bar plot
cars_per_manufacturer_bar = px.bar(
    cars_per_manufacturer,
    x="manufacturer", 
    y="count",
    title="Number of Cars Per Manufacturer",
    labels={"manufacturer": "Car Manufacturer", "count": "Number of Cars"},
    color="manufacturer",  # Different color for each manufacturer
    color_discrete_sequence=px.colors.qualitative.Set3  # Set color scheme
)
st.plotly_chart(cars_per_manufacturer_bar)

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

# Display Plot
st.plotly_chart(fig)