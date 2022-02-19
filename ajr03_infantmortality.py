import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Infant Mortality Rate Web App')
st.markdown('This app help visualize how infant mortality rate varies between different countries from 1960 to 2020.')

@st.cache
def load_data():
	url = 'https://stats.oecd.org/sdmx-json/data/DP_LIVE/.INFANTMORTALITY.../OECD?contentType=csv&detail=code&separator=comma&csv-lang=en'
	df = pd.read_csv(url)
	return df

df = load_data()


st.subheader('Dataset')

st.markdown('The infant mortality rate is defined as the number of deaths of children under one year of age, expressed per 1,000 live births.')

year_options = df['TIME'].unique().tolist()
year = st.selectbox('Which year would you like to see?', year_options, 0)
df_year = df[df['TIME'] == year]

st.write(df_year)
st.markdown('Link to Dataset: https://data.oecd.org/healthstat/infant-mortality-rates.htm#indicator-chart')




# Scatter Plot
st.subheader('Infant mortality rate difference among various countries over time')
fig1 = px.scatter(df, x="Value", y="LOCATION", color = "LOCATION", hover_name="LOCATION",
                 animation_frame="TIME", animation_group="LOCATION",
                 range_x=[0,170],labels=dict(LOCATION="Country", Value="Infant Mortality Rate (Total Deaths/1000 live births)"),
                 width=750, height=1000)

st.write(fig1)




# Bar Plot
title_1 = st.subheader('Infant mortality rate bar plot')

country_options = df['LOCATION'].unique().tolist()
country = st.multiselect('Please enter the country code of the country you would like to see:', options=country_options, default=['MEX', 'BRA', 'CHL', 'IND', 'IDN'])

title_1.subheader('Infant mortality rate bar plot for: '+ ' , '.join(country))

df_country = df[df['LOCATION'].isin(country)]

fig2 = px.bar(df_country, x="LOCATION", y="Value", color="LOCATION",
animation_frame="TIME", animation_group="LOCATION", width=750, height=750, range_y=[0,170],
             labels=dict(LOCATION="Country", Value="Infant Mortality Rate (Total Deaths/1000 live births)"))

st.write(fig2)




# Choropleth Map
title_2 = st.subheader('Infant Mortality Rate Choropleth Map')

year_options_1 = df['TIME'][df['TIME']< df['TIME'].max()].unique().tolist()
year_options_2 = df['TIME'].unique()

year_start = st.selectbox('Select the start year:', year_options_1, year_options_1.index(1990))

year_options_3 = year_options_2[year_options_2 > year_start].tolist()

year_end = st.selectbox('Select the end year:', year_options_3, year_options_3.index(2020))

title_2.subheader(f'Infant Mortality Rate Choropleth Map from {year_start} to {year_end}')

fig3 = px.choropleth(df[(df['TIME']<year_end) & (df['TIME']>=year_start)], locations="LOCATION",color="Value", hover_name="LOCATION", animation_frame="TIME",
             color_continuous_scale=px.colors.sequential.deep, scope = "world", range_color=[1,160],
             labels=dict(Value="Total Deaths/1000 live births"))


st.write(fig3)