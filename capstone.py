dimport streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Customer Sales Analytics', layout='wide', page_icon='📊')

# Header
st.title('📊 Customer Sales Analytics Dashboard')
st.markdown('Track revenue, customers, and product performance in real time.')

# Load data
df = pd.read_csv(r'C:\Users\Bobby\Downloads\Python\Sample - Superstore.csv', encoding='latin1')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month_name()

# Sidebar
st.sidebar.image('https://via.placeholder.com/150x50/2563B8/FFFFFF?text=CellSmart', width=150)
st.sidebar.header('Filters')
year = st.sidebar.multiselect('Year', sorted(df['Year'].unique()), default=sorted(df['Year'].unique()))
region = st.sidebar.multiselect('Region', df['Region'].unique(), default=df['Region'].unique())
segment = st.sidebar.multiselect('Segment', df['Segment'].unique(), default=df['Segment'].unique())

filtered = df[df['Year'].isin(year) & df['Region'].isin(region) & df['Segment'].isin(segment)]

# KPIs
st.subheader('Key metrics')
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric('Revenue', f"${filtered['Sales'].sum():,.0f}")
col2.metric('Profit', f"${filtered['Profit'].sum():,.0f}")
col3.metric('Orders', filtered['Order ID'].nunique())
col4.metric('Customers', filtered['Customer ID'].nunique())
col5.metric('Margin', f"{filtered['Profit'].sum()/filtered['Sales'].sum()*100:.1f}%")

st.divider()

# Row 1
col6, col7 = st.columns(2)

with col6:
    revenue_trend = filtered.groupby('Order Date')['Sales'].sum().reset_index()
    fig1 = px.line(revenue_trend, x='Order Date', y='Sales', title='Revenue over time')
    fig1.update_traces(line_color='#2563B8')
    st.plotly_chart(fig1, use_container_width=True)

with col7:
    segment_sales = filtered.groupby('Segment')['Sales'].sum().reset_index()
    fig2 = px.pie(segment_sales, values='Sales', names='Segment', title='Revenue by segment',
                  color_discrete_sequence=['#2563B8', '#1D9E75', '#D85A30'])
    st.plotly_chart(fig2, use_container_width=True)

# Row 2
col8, col9 = st.columns(2)

with col8:
    category_profit = filtered.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    fig3 = px.bar(category_profit, x='Category', y=['Sales', 'Profit'], barmode='group',
                  title='Sales vs profit by category')
    st.plotly_chart(fig3, use_container_width=True)

with col9:
    top_customers = filtered.groupby('Customer Name')['Sales'].sum().nlargest(10).reset_index()
    fig4 = px.bar(top_customers, x='Sales', y='Customer Name', orientation='h',
                  title='Top 10 customers', color='Sales', color_continuous_scale='blues')
    fig4.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig4, use_container_width=True)

# Download
st.divider()
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button('Download filtered data', csv, 'analytics_export.csv', 'text/csv')