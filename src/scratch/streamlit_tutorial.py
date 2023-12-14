import streamlit_tutorial as st

x = st.slider('Select a value')
st.write(x, 'squared is', x * x)
