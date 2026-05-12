import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Sales Dashboard', layout='wide')
st.title('Sales Dashboard')

df = pd.read_csv('Sample - Superstore.csv', encoding='latin1')
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Sidebar filters
st.sidebar.header('Filters')
region = st.sidebar.multiselect('Region', df['Region'].unique(), default=df['Region'].unique())
category = st.sidebar.multiselect('Category', df['Category'].unique(), default=df['Category'].unique())

filtered = df[df['Region'].isin(region) & df['Category'].isin(category)]

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric('Total Sales', f"${filtered['Sales'].sum():,.0f}")
col2.metric('Total Profit', f"${filtered['Profit'].sum():,.0f}")
col3.metric('Total Orders', filtered['Order ID'].nunique())
col4.metric('Profit Margin', f"{(filtered['Profit'].sum() / filtered['Sales'].sum() * 100):.1f}%")

# Charts
col5, col6 = st.columns(2)

with col5:
    sales_by_category = filtered.groupby('Category')['Sales'].sum().reset_index()
    fig1 = px.bar(sales_by_category, x='Category', y='Sales', color='Category', title='Sales by category')
    st.plotly_chart(fig1, use_container_width=True)

with col6:
    sales_by_region = filtered.groupby('Region')['Sales'].sum().reset_index()
    fig2 = px.pie(sales_by_region, values='Sales', names='Region', title='Sales by region')
    st.plotly_chart(fig2, use_container_width=True)

sales_over_time = filtered.groupby('Order Date')['Sales'].sum().reset_index()
fig3 = px.line(sales_over_time, x='Order Date', y='Sales', title='Sales over time')
st.plotly_chart(fig3, use_container_width=True)

st.subheader('Raw data')
st.dataframe(filtered)

# Top 10 products by sales
st.subheader('Top 10 products by sales')
top_products = filtered.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index()
fig4 = px.bar(top_products, x='Sales', y='Product Name', orientation='h',
              title='Top 10 products', color='Sales', color_continuous_scale='blues')
fig4.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig4, use_container_width=True)

# Profit by sub-category
st.subheader('Profit by sub-category')
profit_sub = filtered.groupby('Sub-Category')['Profit'].sum().reset_index()
profit_sub = profit_sub.sort_values('Profit')
fig5 = px.bar(profit_sub, x='Profit', y='Sub-Category', orientation='h',
              color='Profit', color_continuous_scale='RdYlGn',
              title='Profit by sub-category')
st.plotly_chart(fig5, use_container_width=True)

# Download button
st.subheader('Download filtered data')
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button('Download CSV', csv, 'filtered_sales.csv', 'text/csv')
