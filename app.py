import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Titanic Dashboard', layout='wide')
st.title('Titanic Survival Dashboard')
st.write('Exploring survival patterns from the Titanic dataset.')

df = pd.read_csv(r'C:\Users\Bobby\Downloads\Titanic-Dataset.csv')
df = df.drop(columns=['Cabin'])
df = df.assign(Age=df['Age'].fillna(df['Age'].median()))
df = df.assign(Embarked=df['Embarked'].fillna(df['Embarked'].mode()[0]))

# Sidebar filters
st.sidebar.header('Filters')
selected_class = st.sidebar.multiselect('Passenger class', [1, 2, 3], default=[1, 2, 3])
selected_sex = st.sidebar.multiselect('Sex', ['male', 'female'], default=['male', 'female'])

filtered = df[df['Pclass'].isin(selected_class) & df['Sex'].isin(selected_sex)]

# Metrics row
col1, col2, col3 = st.columns(3)
col1.metric('Total passengers', len(filtered))
col2.metric('Survivors', filtered['Survived'].sum())
col3.metric('Survival rate', f"{filtered['Survived'].mean():.1%}")

# Charts
col4, col5 = st.columns(2)

with col4:
    fig1 = px.bar(filtered.groupby('Sex')['Survived'].mean().reset_index(),
                  x='Sex', y='Survived',
                  color='Sex',
                  color_discrete_map={'male': 'steelblue', 'female': 'salmon'},
                  title='Survival rate by sex')
    fig1.update_yaxes(range=[0, 1])
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    fig2 = px.bar(filtered.groupby('Pclass')['Survived'].mean().reset_index(),
                  x='Pclass', y='Survived',
                  color='Pclass',
                  title='Survival rate by class')
    fig2.update_yaxes(range=[0, 1])
    st.plotly_chart(fig2, use_container_width=True)

st.subheader('Passenger data')
st.dataframe(filtered[['Name', 'Sex', 'Age', 'Pclass', 'Fare', 'Survived']])
