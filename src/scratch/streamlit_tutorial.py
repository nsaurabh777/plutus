import pandas as pd
import numpy as np
import streamlit as st

import plotly.figure_factory as ff
from PIL import Image

x = st.slider('Select a value')
st.write(x, 'squared is', x * x)

# Title widget
st.title('This is a title')

# plain text wideget
st.text("This is some text")

# Code widget example in python language
code = '''def hello():
    print("Hello, Streamlit!")'''

st.code(code, language='python')

# Latex widget example
st.latex(r'''
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
    ''')

# to display pandas dataframe object
df = pd.DataFrame(
   np.random.randn(50, 20),
   columns=('col %d' % i for i in range(20)))

st.dataframe(df)

st.json({
    'foo': 'bar',
    'baz': 'boz',
    'stuff': [
        'stuff 1',
        'stuff 2',
        'stuff 3',
        'stuff 5',
    ],
})

# Example of line chart
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)

# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
fig = ff.create_distplot(
        hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!
st.plotly_chart(fig, use_container_width=True)

# radio widget to take inputs from mulitple options
genre = st.radio(
    "What's your favorite movie genre",
    ('Comedy', 'Drama', 'Documentary'))

if genre == 'Comedy':
    st.write('You selected comedy.')
else:
    st.write("You didn't select comedy.")

# Usage of multiselect widget
options = st.multiselect(
    'What are your favorite colors',
    ['Green', 'Yellow', 'Red', 'Blue'],
    ['Yellow', 'Red'])

st.write('You selected:', options)

# Displaying images on the front end
image = Image.open('/Users/saurabhnair/Downloads/WhatsApp Image 2023-11-18 at 1.24.38 PM.jpeg')

st.image(image, caption='Sunrise by the mountains')
