import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st

import plotly.express as px
# import plotly.figure_factory as ff
# from PIL import Image


# --- Building the app ---

# Set Page Layout
st.set_page_config(layout='wide')

#-----------------------------------------------------------------------
# Load the Dataset
df = sns.load_dataset('tips')

# Add Lat Long
latlong = {'NY': {'lat': 40.730610, 'lon': -73.935242},
           'London': {'lat': 51.509865,'lon': -0.118092},
           'Paris': {'lat': 48.864716, 'lon':2.349014},
           'Sao Paulo': {'lat': -23.533773,'lon': -46.625290},
           'Rome': {'lat': 41.902782,'lon': 12.496366}
           }

city = ['Paris', 'London', 'NY', 'Sao Paulo', 'Rome']
np.random.seed(12)
city_random = np.random.choice(city, 244)

# Add Cols
df['city'] = city_random
df['lat'] = [latlong[city]['lat'] for city in city_random]
df['lon'] = [latlong[city]['lon'] for city in city_random]

#-----------------------------------------------------------------------

# SIDEBAR
# Let's add some functionalities in a sidebar

st.sidebar.subheader('Select to Filter the data')

# By Sex
st.sidebar.text('By Sex')
filter_sex = st.sidebar.radio('Filter By Sex', options=['Both', 'Female', 'Male'])
if filter_sex == 'Both':
    pass
else:
    df = df.query('sex == @filter_sex')

# By City
st.sidebar.text('By City')
filter_city = st.sidebar.multiselect('Filter By City', options=city, default=city)
df = df.query('city in @filter_city')

# About Me
st.sidebar.markdown('---')

st.sidebar.markdown('Demonstration App created with')
st.sidebar.markdown('the toy dataset *Tips* from seaborn')

st.sidebar.text('App created by Saurabh Nair')
st.sidebar.markdown('[Check out my Github](https://github.com/nsaurabh777)')

#-----------------------------------------------------------------------

# Title
st.title('Restaurants Dashboard')

# Subheader
st.subheader('A quick view of the ***Good Meal*** restaurants around the world.')
st.subheader('| About Us')

# Another way to write text
"""
The *Good Meal* restaurants is an international chain founded in 2020 and currently present in 5 of the most important cities in the world: *NYC, São Paulo, London, Paris and Rome*.
"""

#Separator
st.markdown('---')

#-----------------------------------------------------------------------

# Columns Summary

st.subheader('| QUICK SUMMARY')
st.write(df.sample(3))

col1, col2, col3, col4 = st.columns(4)
# column 1 - Revenue Sum
with col1:
    total = f'${int( df.total_bill.sum() ):,}'
    st.title(total)
    st.text('REVENUE')
# column 2 - Count of meals
with col2:
    st.title(df.city.count())
    st.text('MEALS')
# column 3 - Sum of clients
with col3:
    st.title(df['size'].sum())
    st.text('CLIENTS')
# column 4 - Count of cities
with col4:
    st.title(df.city.nunique())
    st.text('CITIES')

#-----------------------------------------------------------------------

# Graphics
col1, col2, col3 = st.columns(3)
# column 1 - Pie chart Gender
with col1:
    ind1 = pd.DataFrame(df.groupby('sex').sex.count()).rename(columns={'sex':'count'}).reset_index()
    g1 = px.pie(ind1,
                values='count',
                names='sex',
                color='sex',
                color_discrete_map={'Male': 'royalblue','Female': 'pink'},
                title='| GENDER')
    g1.update_traces(textposition='inside',
                     textinfo='percent+label',
                     showlegend=False)
    st.plotly_chart(g1, use_container_width=True)

# column 2 - Bar chart Count Meals By day
with col2:
    ind3 = pd.DataFrame(df.groupby('day').day.count()).rename(columns={'day':'count'}).reset_index(
        ).sort_values('count', ascending=False)
    g3 = px.bar(ind3,
                x='day',
                y='count',
                color='day',
                title='| POPULAR DAYS')
    g3.update_traces(showlegend=False)
    st.plotly_chart(g3, use_container_width=True)

# column 3 - Pie chart Count Meals By Time
with col3:
    ind2 = pd.DataFrame(df.groupby('time').time.count()).rename(columns={'time':'count'}).reset_index()
    g2 = px.pie(ind2,
                values='count',
                names='time',
                color='time',
                color_discrete_map={'Lunch': 'royalblue','Dinner': 'darkblue'},
                title='| POPULAR TIMES')
    g2.update_traces(textposition='inside',
                     textinfo='percent+label',
                     showlegend=False)
    st.plotly_chart(g2, use_container_width=True)

#-----------------------------------------------------------------------
st.subheader('| WHERE ARE WE MAKING MORE MONEY')
# Measurements
col1, col2 = st.columns(2)
# column 1 X Axis
with col1:
    # print(df.info())
    categorical_cols = pd.DataFrame(df.select_dtypes(include=['object', 'category'])).columns
    numerical_cols = pd.DataFrame(df.select_dtypes(include=['int64', 'float64'])).columns
    # print(f"categorical_cols: {categorical_cols}, {len(categorical_cols)}\n"
    #       f"numerical_cols: {numerical_cols}, {len(numerical_cols)}")
    x = st.selectbox('Select the X Axis', options=categorical_cols, index=len(categorical_cols)-1)
# column 2 Y axis
with col2:
    y = st.selectbox('Select the Y Axis', options=list(set(numerical_cols) - {'lat', 'lon'}))

# Show mean checkbox
mean_yes = st.checkbox('Mean')
if mean_yes:
           df_mean = pd.pivot_table(df, index=x, values=y, aggfunc=np.mean).reset_index()
           g4 = px.bar(df_mean,
            x= x,
            y= y)
           st.plotly_chart(g4, use_container_width=True)
else:
           g4 = px.bar(df,
                       x= x,
                       y= y)
           st.plotly_chart(g4, use_container_width=True)

#-----------------------------------------------------------------------

# Map
st.subheader('| WHERE ARE OUR RESTAURANTS')
df_map = df[['city','tip','lat', 'lon']]
st.map(df_map, zoom=2)

#-----------------------------------------------------------------------


# # Title widget
# st.title('This is a title')
# # Subheader
# st.subheader("Here, a subheader")
# # Text
# st.text("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam eget ligula eu lectus lobortis condimentum.")
# # Using st.write
# st.write("This is can be used for text and other features.")
# # plain text widget
# st.text("This is some text")
#
# # Code widget example in python language
# code = '''def hello():
#     print("Hello, Streamlit!")'''
#
# st.code(code, language='python')
#
# # Latex widget example
# st.latex(r'''
#     a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
#     \sum_{k=0}^{n-1} ar^k =
#     a \left(\frac{1-r^{n}}{1-r}\right)
#     ''')
#
# # Slider
# x = st.slider('Select a value')
# st.write(x, 'squared is', x * x)
#
# # to display pandas dataframe object
# df = pd.DataFrame(
#    np.random.randn(50, 20),
#    columns=('col %d' % i for i in range(20)))
#
# st.dataframe(df)
#
# st.json({
#     'foo': 'bar',
#     'baz': 'boz',
#     'stuff': [
#         'stuff 1',
#         'stuff 2',
#         'stuff 3',
#         'stuff 5',
#     ],
# })
#
# # Example of line chart
# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=['a', 'b', 'c'])
#
# st.line_chart(chart_data)
#
# # Add histogram data
# x1 = np.random.randn(200) - 2
# x2 = np.random.randn(200)
# x3 = np.random.randn(200) + 2
#
# # Group data together
# hist_data = [x1, x2, x3]
#
# group_labels = ['Group 1', 'Group 2', 'Group 3']
#
# # Create distplot with custom bin_size
# fig = ff.create_distplot(
#         hist_data, group_labels, bin_size=[.1, .25, .5])
#
# # Plot!
# st.plotly_chart(fig, use_container_width=True)
#
# # radio widget to take inputs from mulitple options
# genre = st.radio(
#     "What's your favorite movie genre",
#     ('Comedy', 'Drama', 'Documentary'))
#
# if genre == 'Comedy':
#     st.write('You selected comedy.')
# else:
#     st.write("You didn't select comedy.")
#
# # Usage of multiselect widget
# options = st.multiselect(
#     'What are your favorite colors',
#     ['Green', 'Yellow', 'Red', 'Blue'],
#     ['Yellow', 'Red'])
#
# st.write('You selected:', options)
#
# # Displaying images on the front end
# image = Image.open('/Users/saurabhnair/Downloads/WhatsApp Image 2023-11-18 at 1.24.38 PM.jpeg')
#
# st.image(image, caption='Sunrise by the mountains')
#
#
# # --- https://medium.com/gustavorsantos/streamlit-basics-build-your-first-web-app-ffd377a85666 ---
# # Load Dataset
# df = sns.load_dataset('tips')
# # Page Title
# st.title('Examples of what st.write() can do')
# # Text + emoji
# st.write('Hello :sunglasses: :heart: ')
# # Calculations
# st.write(1+1)
# # Variables
# a = 2**2
# st.write(a)
# # Table
# st.write(df.head(2))
# # Multiple
# st.write('st.write("text", df)', df.head(3))
#
#
# # Add Lat Long
# latlong = {'NY': {'lat': 40.730610, 'lon': -73.935242},
#            'London': {'lat': 51.509865,'lon': -0.118092},
#            'Paris': {'lat': 48.864716, 'lon':2.349014},
#            'Sao Paulo': {'lat': -23.533773,'lon': -46.625290},
#            'Rome': {'lat': 41.902782,'lon': 12.496366}
#            }
# city = ['Paris', 'London', 'NY', 'Sao Paulo', 'Rome']
# city_random = np.random.choice(city, 244)
# # Add Cols
# df['city'] = city_random
# df['lat'] = [latlong[city]['lat'] for city in city_random]
# df['lon'] = [latlong[city]['lon'] for city in city_random]
# # Map
# map_df = df[['lat', 'lon']]
# st.map(map_df, zoom=1)
