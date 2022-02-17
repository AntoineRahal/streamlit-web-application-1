import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Infant Mortality Web App')
st.markdown('The infant mortality rate is defined as the number of deaths of children under one year of age, expressed per 1,000 live births.')

@st.cache
def load_data():
	url = 'https://stats.oecd.org/sdmx-json/data/DP_LIVE/.INFANTMORTALITY.../OECD?contentType=csv&detail=code&separator=comma&csv-lang=en'
	df = pd.read_csv(url)
	return df

df = load_data()


st.subheader('Infant Mortality Rates Dataset')

#st.write(df)

year_options = df['TIME'].unique().tolist()
year = st.selectbox('Which year would you like to see?', year_options, 0)
df_year = df[df['TIME'] == year]

st.write(df_year)




# Scatter Plot
st.subheader('Scatter')
fig1 = px.scatter(df, x="Value", y="LOCATION", color = "LOCATION", hover_name="LOCATION",
                 animation_frame="TIME", animation_group="LOCATION",
                 range_x=[0,170],labels=dict(LOCATION="Country", Value="Infant Mortality Rate (Total Deaths/1000 live births)"),
                 width=750, height=750)

st.write(fig1)




# Bar Plot
st.subheader('First Plot')

country_options = df['LOCATION'].unique().tolist()
country = st.multiselect('Please enter the country code of the country you would like to see', options=country_options, default=['MEX', 'BRA', 'CHL', 'IND', 'IDN'])

df_country = df[df['LOCATION'].isin(country)]

fig2 = px.bar(df_country, x="LOCATION", y="Value", color="LOCATION",
animation_frame="TIME", animation_group="LOCATION", width=750, height=750, range_y=[0,170],
             labels=dict(LOCATION="Country", Value="Infant Mortality Rate (Total Deaths/1000 live births)"))

st.write(fig2)




# Choropleth Map
st.subheader('Map')
fig3 = px.choropleth(df[(df['TIME']<2020) & (df['TIME']>=1990)], locations="LOCATION",color="Value", hover_name="LOCATION", animation_frame="TIME",
             color_continuous_scale=px.colors.sequential.deep, scope = "world", range_color=[1,160],
             labels=dict(Value="Total Deaths/1000 live births"))


st.write(fig3)