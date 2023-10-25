# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: passunca <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/10/24 08:48:10 by passunca          #+#    #+#              #
#    Updated: 2023/10/25 12:10:56 by passunca         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import streamlit as st
import pandas as pd
import datetime

# Import DB
df = pd.read_csv("assets/sogrape.csv")
stores_list = df["Store Name"].unique()
stores_location = df["Location"].unique()

# DB Connection
conn = st.experimental_connection('sogrape_db', type='sql')

# Query and display the data 
wine_table = conn.query('select * from wine_table')
st.dataframe(wine_table)

# Session State
# if 'update_db' not in st.session_state:
#     st.session_state.update_db = False

# App Header
st.header("Hack'a'Wine Dashboard 🍷")

# Init Tabs
scrapper_tab, analyser_tab = st.tabs(["Scraper", "Analyser"])
# Init Cols
scrapper_col1, scrapper_col2 = scrapper_tab.columns(2)
analyser_col1, analyser_col2 = analyser_tab.columns(2)

# Calculations
# Get price average by store 
average_prices = df.groupby('Store Name')['Price'].mean()
# Convert Series into DataFrame
average_prices_df = average_prices.reset_index()

# Data
with st.sidebar:
    st.image(
        "assets/sogrape.png",
        width=150
    )
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
    st.button(
        "Scrape & Update DB 🔄", 
        # on_click=None
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
    # Filtered Discount (show only True)
    discount_true = filtered_df['Discount'] == True
    filtered_df_discount = filtered_df.loc[discount_true ]


# Scraper TAB
with scrapper_tab:
    st.dataframe(
        filtered_df,
        hide_index=True,
    )

# Analyser TAB
with analyser_tab:
    # Price Graphs
    with st.expander("Price Graphs 📊"):
        st.write("Prices by Location 📍")
        st.bar_chart(filtered_df, x="Price", y="Location")
        st.write("Price by Harvest Year 🪙")
        st.bar_chart(filtered_df_discount, x="Harvest Year", y="Price")
        st.write("Average Price by Store 🪙")
        st.bar_chart(average_prices_df, x="Store Name", y="Price")
    # Left column
    with analyser_col1:
        with st.expander("Discount Graphs 📊"):
            # Discount Charts
            st.write("Discounts by Store 📣")
            st.bar_chart(filtered_df, x="Store Name", y="Discount")
    # Right column
    with analyser_col2:
            # Capacity Chart
        with st.expander("Capacity Graphs 📊"):
            st.write("Capacity Overview")
            st.bar_chart(filtered_df, x="Capacity", y="Store Name")
    

