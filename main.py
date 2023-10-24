# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: passunca <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/10/24 08:48:10 by passunca          #+#    #+#              #
#    Updated: 2023/10/24 14:32:57 by passunca         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import streamlit as st
import pandas as pd
import datetime

# Import DB
df = pd.read_csv("MOCK_DATA2.csv")
stores_list = df["Store Name"].unique()
stores_location = df["Location"].unique()

# Init Tabs
scrapper_tab, analyser_tab = st.tabs(["Scrapper", "Analyser"])
# Init Cols
scrapper_col1, scrapper_col2 = scrapper_tab.columns(2)
analyser_col1, anaylser_col2 = scrapper_tab.columns(2)

# Data
with st.sidebar:
    st.header("Filter Wine Data")
    selected_store = st.selectbox('by Store', stores_list)
    selected_location = st.selectbox('by Location', stores_location)
    
    st.slider(
        "by Harvest Date", 
        min_value=df["Harvest Year"].min(),
        max_value=df["Harvest Year"].max(),
        key="harvest-date-slider" 
    )
    st.slider(
        "by Price",
        min_value=df["Price"].min(),
        max_value=df["Price"].max(),
        key="price-slider"
    )

# Scrapper TAB
with scrapper_tab:
    with st.expander("View Raw Data"):
        st.dataframe(
            df,
            hide_index=True,
        )

    # Prices Chart
    st.title("Prices Overview")
    st.area_chart(df, y="Price")

# Analyser TAB
with analyser_tab:
    st.header("Data Analyser")

