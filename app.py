import plotly.express as px
import streamlit as st
from pandas.core.computation.common import result_type_many
import plotly.graph_objects as go
import pandas as pd
from dbhelper import DB

db = DB()

st.sidebar.title('Aviation Analytics')
user_option = st.sidebar.selectbox('Menu', ['Select one', 'Check Flights', 'Analytics'])

if user_option == 'Check Flights':
    st.title('Check Flights')
    col1, col2 = st.columns(2)

    with col1:
        city = db.fetch_city_names()
        source = st.selectbox('Source', sorted(city))
    with col2:
        destination = st.selectbox('Destination',sorted(city))

    if st.button('Search'):
        result = db.fetch_all_flights(source,destination)
        if len(result)==0:
            st.write("No Flights Available")
        else:
            st.dataframe(result)


elif user_option == 'Analytics':
    st.title('Share of each airline in total number of flights')
    airline , frequency = db.fetch_count_flights()
    fig = go.Figure(
        go.Pie(
            labels = airline,
            values = frequency,
            hoverinfo="label+percent",
            textinfo="value"
        )
    )
    st.header("pie chart")
    st.plotly_chart(fig)


    airports, num_flights = db.busy_airports()
    fig1 = go.Figure(
        go.Bar(
            x=airports,
            y=num_flights,
            text=num_flights,
            textposition="auto"
        )
    )
    st.header("List of the busiest airports")
    st.plotly_chart(fig1)


    # Fetch data from the database
    date, count_flights = db.flights_per_day()
    fig = px.line(
        x= date,
        y=count_flights
    )
    st.plotly_chart(fig,theme="streamlit",use_container_width=True)

