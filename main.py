# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: passunca <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/10/24 08:48:10 by passunca          #+#    #+#              #
#    Updated: 2023/10/24 12:21:58 by passunca         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import streamlit as st
import pandas as pd

# Import DB
df = pd.read_csv("MOCK_DATA2.csv")
stores_list = df["Store Name"].unique()

# Init Tabs
scrapper_tab, analyser_tab = st.tabs(["Scrapper", "Analyser"])
# Init Cols
scrapper_col1, scrapper_col2 = scrapper_tab.columns(2)
analyser_col1, anaylser_col2 = scrapper_tab.columns(2)

# Data
stores = ["Store 1", "Store 2", "Store 3"]

with st.sidebar:
    st.header("Filter Wine Data")
    st.selectbox('Filter by Store', stores_list)
    st.title("Filter by Location")
    st.selectbox('Filter by Location', stores)
    
    st.title("Filter by Harvest Date")
    st.slider("Select", 0, 10, 5)

    st.title("Filter by Harvest Price")

with scrapper_tab:
    st.header("Data Scrapper")
    df = pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
    })

df

with analyser_tab:
    st.header("Data Analyser")

