# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: passunca <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/10/24 08:48:10 by passunca          #+#    #+#              #
#    Updated: 2023/10/25 09:24:06 by passunca         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import streamlit as st
import pandas as pd
import datetime
from forex_python.converter import CurrencyRates

# Import DB
df = pd.read_csv("MOCK_DATA2.csv")
stores_list = df["Store Name"].unique()
stores_location = df["Location"].unique()

# Init currency converter
c = CurrencyRates()

# Session State
if 'update_db' not in st.session_state:
    st.session_state.update_db = False


# App Header
st.header("Hack'a'Wine Dashboard 🍷")

# Init Tabs
scrapper_tab, analyser_tab = st.tabs(["Scrapper", "Analyser"])
# Init Cols
scrapper_col1, scrapper_col2 = scrapper_tab.columns(2)
analyser_col1, anaylser_col2 = scrapper_tab.columns(2)

# Calculations
# Get price average by store 
average_prices = df.groupby('Store Name')['Price'].mean()
# Convert Series into DataFrame
average_prices_df = average_prices.reset_index()

# Data
with st.sidebar:
    st.header("Filter Wine Data")
    selected_wine = st.multiselect('by Wine Name 🍷', df["Wine Name"].unique())
    selected_store = st.multiselect('by Store 🏪', stores_list)
    selected_location = st.multiselect('by Location 🗺', stores_location)
    
    selected_date_range = st.slider(
        "by Harvest Date ⏲", 
        min_value=int(df["Harvest Year"].min()),
        max_value=int(df["Harvest Year"].max()),
        value=(int(df["Harvest Year"].min()), int(df["Harvest Year"].max())),
        key="harvest-date-slider" 
    )
    selected_price_range = st.slider(
        "by Price 💰",
        min_value=float(df["Price"].min()),
        max_value=float(df["Price"].max()),
        value=(float(df["Price"].min()), float(df["Price"].max())),
        key="price-slider"
    )

    filtered_df = df
    # Wine Filter
    if selected_wine:
        filtered_df = filtered_df[(filtered_df['Wine Name'].isin(selected_wine))]
    # Store Filter
    if selected_store:  
        filtered_df = filtered_df[(filtered_df['Store Name'].isin(selected_store))]
    # Location Filter
    if selected_location:
        filtered_df = filtered_df[(filtered_df['Location'].isin(selected_location))]
    # Harvest Year Filter
    filtered_df = filtered_df[(filtered_df['Harvest Year'] >= selected_date_range[0]) & (filtered_df['Harvest Year'] <= selected_date_range[1])]
    # Price Filter
    filtered_df = filtered_df[(filtered_df['Price'] >= selected_price_range[0]) & (filtered_df['Price'] <= selected_price_range[1])]


# Scrapper TAB
with scrapper_tab:
    st.button("Update DB 🔄", on_click=st.session_state.update_db)
    # Left column
    with scrapper_col1:
        # Prices Charts
        with st.expander("Price Graphs 📊"):
            st.write("Prices by Location 📍")
            st.bar_chart(filtered_df, x="Price", y="Location")
            st.write("Average Price by Store 🪙")
            st.bar_chart(average_prices_df, x="Store Name", y="Price")
    # Right column
    with scrapper_col2:
            # Capacity Chart
        with st.expander("Capacity Graphs 📊"):
            st.write("Capacity Overview")
            st.bar_chart(filtered_df, x="Capacity", y="Store Name")


# Analyser TAB
with analyser_tab:
    # Raw Data Table
    with st.expander("View Raw Data 🧾"):
        st.dataframe(
            filtered_df,
            hide_index=True,
        )
    
    st.area_chart(df, y="Price")

