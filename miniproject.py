import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

#background
st.markdown(
    """
    <style>
    .stApp {background-color: #2c2c2c;}
    </style>
    """,
    unsafe_allow_html=True
)

tab1, tab2 = st.tabs(["📊 Dashboard", "📋 Data Table"])

with tab2:

# import data
    df = pd.read_csv(r"C:\Users\User\Downloads\sales_data.csv")

# clean data
    df = df.drop(['Region', 'Unit_Cost', 'Customer_Type', 'Payment_Method', 'Sales_Channel', 'Region_and_Sales_Rep'], axis=1)
    df = df.rename(columns={'Product_ID': 'Product ID', 
                        'Sale_Date': 'Sale Date', 
                        'Sales_Rep': 'Customer', 
                        'Sales_Amount': 'Sales Amount', 
                        'Quantity_Sold': 'Quantity Sold', 
                        'Product_Category': 'Product Category', 
                        'Unit_Price': 'Unit Price',
                        'Customer_Type': 'Customer Type', 
                        'Product_Category': 'Product Category',
                       })
    df['Sales Amount'] = df['Unit Price'] * df['Quantity Sold'] * (1 - df['Discount'])
    df['Sales Amount'] = df['Sales Amount'].round(2)
    df['Sale Date'] = pd.to_datetime(df['Sale Date'], errors='coerce')

    st.sidebar.header("🔎 Filter Data")

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #2c2c2c;
        }
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] select,
        [data-testid="stSidebar"] textarea,
        [data-testid="stSidebar"] .stMultiSelect,
        [data-testid="stSidebar"] .stDateInput {
            background-color: #2c2c2c !important;
            color: white !important;
            border: 1px solid #444 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    category = st.sidebar.multiselect(
            "Select Product Category",
            options=df["Product Category"].unique(),
            default=df["Product Category"].unique()
        )
    customer = st.sidebar.multiselect(
            "Select Customer",
            options=df["Customer"].unique(),
            default=df["Customer"].unique()
        )
    date_range = st.sidebar.date_input(
            "Select Date Range",
            [df["Sale Date"].min(), df["Sale Date"].max()]
        )
    filtered_df = df[
            (df["Product Category"].isin(category)) &
            (df["Customer"].isin(customer)) &
            (df["Sale Date"] >= pd.to_datetime(date_range[0])) &
            (df["Sale Date"] <= pd.to_datetime(date_range[1]))
        ]
    
    search_query = st.text_input("🔍 Search for a Customer or Product:")
    if search_query:
        filtered_df = df[df.apply(lambda row: search_query.lower() in row.astype(str).str.lower().to_string(), axis=1)]
    else:
        filtered_df = df
    st.dataframe(filtered_df)

with tab1: 

    # insert image
    st.image('AZ logo.png')

    # title
    st.markdown("<h1 style='color: white;'>📊📈 Supermarket Sales 📊📈</h1>", unsafe_allow_html=True)

    # key metrics (KPIs)
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(
        "<span style='color:white; font-weight:bold;'>💰 Total Sales</span><br>"
        f"<span style='color:gold; font-size:24px;'>${df['Sales Amount'].sum():,.2f}</span>",
        unsafe_allow_html=True)
    col2.markdown(
        "<span style='color:white; font-weight:bold;'>👥 Total Customers</span><br>"
            f"<span style='color:gold; font-size:24px;'>{df['Customer'].nunique()}</span>",
        unsafe_allow_html=True)
    col3.markdown(
        "<span style='color:white; font-weight:bold;'>📦 Quantity Sold</span><br>"
        f"<span style='color:gold; font-size:24px;'>{df['Quantity Sold'].sum()}</span>",
        unsafe_allow_html=True)
    col4.markdown(
        "<span style='color:white; font-weight:bold;'>📊 Avg. Sales/Order</span><br>"
        f"<span style='color:gold; font-size:24px;'>${df['Sales Amount'].mean():,.2f}</span>",
        unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:        
        # chart Sales Amount by Customer (Bar)
        fig2 = px.bar(df, x='Customer', y='Sales Amount', title='Sales Amount by Customer')
        fig2.update_layout(
            plot_bgcolor='#2c2c2c',
            paper_bgcolor='#2c2c2c',
            font=dict(color='white'),
            title=dict(
                font=dict(size=24, color='white'),
            ),
            xaxis=dict(color='white', tickangle=-45, showgrid=False),
            yaxis=dict(color='white', showgrid=False),
            legend=dict(font=dict(color='white')),
            hoverlabel=dict(font_color='white', bgcolor='#2c2c2c')
        )
        fig2.update_traces(marker=dict(color='orange'))
        st.plotly_chart(fig2)
        
    with col2:      
        # chart Product Category (pie)
        category_sales = df.groupby('Product Category')['Sales Amount'].sum().reset_index()
        pie_colors = ['#ff0000', '#ff4d00', '#ff9900', '#ffcc00']
        fig4 = px.pie(
            category_sales,
            names='Product Category',
            values='Sales Amount',
            title='Sales Distribution by Product Category',
            hole=0.7,
            color_discrete_sequence=pie_colors
        )
        fig4.update_layout(
            plot_bgcolor='#2c2c2c',
            paper_bgcolor='#2c2c2c',
            font=dict(color='white'),
            title=dict(font=dict(size=24, color='white')),
            legend=dict(font=dict(color='white')),
        )
        st.plotly_chart(fig4)
        
    col3, col4 = st.columns(2)
    
    with col3:
        # chart Daily Sales (line)
        daily_sales = df.groupby('Sale Date')['Sales Amount'].sum().reset_index()
        fig1 = px.line(daily_sales, x='Sale Date', y='Sales Amount', title='Daily Sales Trend')
        fig1.update_layout(
            plot_bgcolor='#2c2c2c',
            paper_bgcolor='#2c2c2c',
            font=dict(color='white'),
            title=dict(
                font=dict(size=24, color='white')
            ),
            xaxis=dict(color='white', showgrid=False),
            yaxis=dict(color='white', showgrid=False),
            legend=dict(font=dict(color='white')),
            hoverlabel=dict(font_color='white', bgcolor='#2c2c2c')
        )
        fig1.update_traces(line_color='red')
        st.plotly_chart(fig1)
        
    with col4:
        # chart Montly Sales (pie)
        df['Month_Name'] = df['Sale Date'].dt.strftime('%B')
        monthly_sales = df.groupby('Month_Name')['Sales Amount'].sum().reset_index()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        monthly_sales['Month_Name'] = pd.Categorical(monthly_sales['Month_Name'], categories=month_order, ordered=True)
        monthly_sales = monthly_sales.sort_values('Month_Name')
        pie_colors = ['#ff0000', '#ff1a00', '#ff3300', '#ff4d00', '#ff6600', '#ff8000',
                      '#ff9900', '#ffb300', '#ffcc00', '#ffe000', '#fff000', '#ffff00']
        fig3 = px.pie(
            monthly_sales,
            names='Month_Name',
            values='Sales Amount',
            title='Monthly Sales Distribution',
            color_discrete_sequence=pie_colors
        )
        fig3.update_layout(
            plot_bgcolor='#2c2c2c',
            paper_bgcolor='#2c2c2c',
            font=dict(color='white'),
            title=dict(
                font=dict(size=24, color='white')
            ),
            legend=dict(font=dict(color='white')),
        )
        st.plotly_chart(fig3)

