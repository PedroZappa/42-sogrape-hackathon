# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: passunca <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/10/24 08:48:10 by passunca          #+#    #+#              #
#    Updated: 2023/10/25 13:23:49 by passunca         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import streamlit as st
import pandas as pd
import datetime

# Import DB
# df = pd.read_csv("assets/sogrape.csv")

# # DB Connection
conn = st.experimental_connection('hackawine_db', type='sql')
# # Query and display the data 
df = conn.query('select * from hackawine_table')

stores_list = df["store_name"].unique()
capacity = df["capacity"].unique()
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
average_prices = df.groupby('store_name')['price'].mean()
# Convert Series into DataFrame
average_prices_df = average_prices.reset_index()

# Data
with st.sidebar:
    st.image(
        "assets/sogrape.png",
        width=150
    )
    st.header("Filter Wine Data")
    selected_wine = st.multiselect('by Wine Name 🍷', df["wine_name"].unique())
    selected_store = st.multiselect('by Store 🏪', stores_list)
    selected_capacity = st.slider(
        'by Capacity 🧴', 
        min_value=float(df["capacity"].min()),
        max_value=float(df["capacity"].max()),
        key="capacity-slider"
    )
    
    selected_date_range = st.slider(
        "by Harvest Date ⏲", 
        value=(int(df["harvest_year"].min()), int(df["harvest_year"].max())),
        key="harvest-date-slider" 
    )

    selected_price_range = st.slider(
        "by Price 💰",
        min_value=float(df["price"].min()),
        max_value=float(df["price"].max()),
        value=(float(df["price"].min()), float(df["price"].max())),
        key="price-slider"
    )
    st.button(
        "Scrape & Update DB 🔄", 
        # on_click=None
    )

    filtered_df = df
    # Wine Filter
    if selected_wine:
        filtered_df = filtered_df[(filtered_df['wine_name'].isin(selected_wine))]
    # Store Filter
    if selected_store:  
        filtered_df = filtered_df[(filtered_df['store_name'].isin(selected_store))]
    # Capacity Filter
    if selected_capacity:
        filtered_df = filtered_df[(filtered_df['location'].isin(selected_capacity))]
    # Harvest Year Filter
    filtered_df = filtered_df[(filtered_df['harvest_year'] >= selected_date_range[0]) & (filtered_df['harvest_year'] <= selected_date_range[1])]
    # Price Filter
    filtered_df = filtered_df[(filtered_df['price'] >= selected_price_range[0]) & (filtered_df['price'] <= selected_price_range[1])]
    # Filtered Discount (show only True)
    discount_true = filtered_df['discount'] == 1
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
        st.bar_chart(filtered_df, x="price", y="location")
        st.write("Price by Harvest Year 🪙")
        st.bar_chart(filtered_df_discount, x="harvest_year", y="price")
        st.write("Average Price by Store 🪙")
        st.bar_chart(average_prices_df, x="store_name", y="price")
    # Left column
    with analyser_col1:
        with st.expander("Discount Graphs 📊"):
            # Discount Charts
            st.write("Discounts by Store 📣")
            st.bar_chart(filtered_df, x="wine_name", y="discount")
    # Right column
    with analyser_col2:
            # Capacity Chart
        with st.expander("Capacity Graphs 📊"):
            st.write("Capacity Overview")
            st.bar_chart(filtered_df, x="capacity", y="store_name")
    

