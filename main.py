# Importing libraries
import streamlit as st
import pandas as pd
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
import plotly.express as px

# Database connection
db_engine = create_engine('mysql+pymysql://root:12345678@localhost/phonepe')

# Fetch data from MySQL
def load_data(query):
    return pd.read_sql(query, db_engine)

# Load data into dataframes
agg_trans_df = load_data("SELECT * FROM aggregated_transactions")
agg_users_df = load_data("SELECT * FROM aggregated_users")
map_trans_df = load_data("SELECT * FROM map_transactions")
map_users_df = load_data("SELECT * FROM map_users")
top_trans_df = load_data("SELECT * FROM top_transactions")
top_users_df = load_data("SELECT * FROM top_users")

# Streamlit App
st.title("PhonePe Pulse Data Visualization")

# Slider for year selection
years = sorted(agg_trans_df['year'].unique()) 
selected_year = st.slider("Select Year", min_value=min(years), max_value=max(years), value=min(years))

# Filter data based on the selected year
agg_trans_df_year = agg_trans_df[agg_trans_df['year'] == selected_year]
agg_users_df_year = agg_users_df[agg_users_df['year'] == selected_year]
map_trans_df_year = map_trans_df[map_trans_df['year'] == selected_year]
map_users_df_year = map_users_df[map_users_df['year'] == selected_year]
top_trans_df_year = top_trans_df[top_trans_df['year'] == selected_year]
top_users_df_year = top_users_df[top_users_df['year'] == selected_year]

# Sidebar for options
option = st.sidebar.selectbox("Choose a data", ["Aggregated", "Map", "Top"])

# Aggregated 
if option == "Aggregated":
    section = st.sidebar.selectbox("Choose a type", ["Transactions", "Users"])

    if section == "Transactions":
        visualize = st.sidebar.selectbox("Choose a visualization",["Choropleth Maps","Bar Chart","Pie Chart"])

        if visualize == "Choropleth Maps":
            st.header("Aggregated Transactions - Choropleth Maps")
            fig = px.choropleth(
                agg_trans_df_year,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='state',
                color='transaction_amount',
                color_continuous_scale='spectral'
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)

        elif visualize == "Bar Chart":
            st.header("Aggregated Transactions - Bar Chart")
            state_data = agg_trans_df_year.groupby('state')['transaction_amount'].sum().reset_index()
            fig = px.bar(
                state_data, 
                x='state', 
                y='transaction_amount', 
                title=f'Total Transaction Amount by State ({selected_year})')
            st.plotly_chart(fig)
            
        elif visualize == "Pie Chart":
            st.header("Aggregated Transactions - Pie Chart")
            state_data = agg_trans_df_year.groupby('state')['transaction_amount'].sum().reset_index()
            fig = px.pie(
                state_data,
                names='state',  
                values='transaction_amount',  
                title=f'Total Transaction Amount by State ({selected_year})'
            )
            st.plotly_chart(fig)

# Map
elif option == "Map":
    section = st.sidebar.selectbox("Choose a type", ["Transactions", "Users"])

    if section == "Transactions":
        visualize = st.sidebar.selectbox("Choose a visualization type",["Choropleth Maps","Bar Chart","Pie Chart"])

        
        if visualize == "Choropleth Maps":
            st.header("Map Transactions - Choropleth Maps")
            fig = px.choropleth(
                map_trans_df_year,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',  
                locations='state',
                color='amount',  
                color_continuous_scale='spectral',
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)

        elif visualize == "Bar Chart":
            st.header("Map Transactions - Bar Chart")
            district_data = map_trans_df_year.groupby('district')['amount'].sum().reset_index()
            fig = px.bar(
                district_data,
                x='district',
                y='amount',
                title=f'Total Transaction Amount by District ({selected_year})',
                labels={'district': 'District', 'amount': 'Transaction Amount'},
                height=400
            )
            st.plotly_chart(fig)

        elif visualize == "Pie Chart":
            st.header("Map Transactions - Pie Chart")
            district_data = map_trans_df_year.groupby('district')['amount'].sum().reset_index()
            fig = px.pie(
                district_data,
                names='district',
                values='amount',
                title=f'Transaction Amount Distribution by District ({selected_year})'
            )
            st.plotly_chart(fig)

    elif section == "Users":
        visualize = st.sidebar.selectbox("Choose a visualization type",["Choropleth Maps","Bar Chart","Pie Chart"])

        if visualize == "Choropleth Maps":
            st.header("Map Users - Choropleth Maps")
            fig = px.choropleth(
                map_users_df_year,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',  
                locations='state',
                color='registered_user',  
                color_continuous_scale='spectral',
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)

        elif visualize == "Bar Chart":
            st.header("Map Users - Bar Chart")
            district_data = map_users_df_year.groupby('district')['registered_user'].sum().reset_index()
            fig = px.bar(
                district_data,
                x='district',
                y='registered_user',
                title=f'Total Registered Users by District ({selected_year})',
                labels={'district': 'District', 'registered_user': 'Registered Users'},
                height=400
            )
            st.plotly_chart(fig)

        elif visualize == "Pie Chart":
            st.header("Map Users - Pie Chart")
            district_data = map_users_df_year.groupby('district')['registered_user'].sum().reset_index()
            fig = px.pie(
                district_data,
                names='district',
                values='registered_user',
                title=f'Registered Users Distribution by District ({selected_year})'
            )
            st.plotly_chart(fig)

# Top 
elif option == "Top":
    section = st.sidebar.selectbox("Choose a type", ["Transactions", "Users"])

    if section == "Transactions":
        visualize = st.sidebar.selectbox("Choose a visualization type", ["Choropleth Maps", "Bar Chart", "Pie Chart"])

        if visualize == "Choropleth Maps":
            st.header("Top Transactions - Choropleth Maps")
            fig = px.choropleth(
                top_trans_df_year,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',  
                locations='state',
                color='district_count',  
                color_continuous_scale='spectral',
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)
           
        elif visualize == "Bar Chart":
            st.header("Top Transactions - Bar Chart")
            district_data = top_trans_df_year.groupby('district')['district_count'].sum().reset_index()
            fig = px.bar(
                district_data,
                x='district',
                y='district_count',
                title=f'Total District Count by District ({selected_year})',
                labels={'district': 'District', 'district_count': 'District Count'},
                height=400
            )
            st.plotly_chart(fig)

        elif visualize == "Pie Chart":
            st.header("Top Transactions - Pie Chart")
            district_data = top_trans_df_year.groupby('district')['district_count'].sum().reset_index()
            fig = px.pie(
                district_data,
                names='district',
                values='district_count',
                title=f'District Count Distribution by District ({selected_year})'
            )
            st.plotly_chart(fig)

    elif section == "Users":
        visualize = st.sidebar.selectbox("Choose a visualization type", ["Choropleth Maps", "Bar Chart", "Pie Chart"])

        if visualize == "Choropleth Maps":
            st.header("Top Users - Choropleth Maps")
            fig = px.choropleth(
                top_users_df_year,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',  
                locations='state',
                color='registered_users',  
                color_continuous_scale='spectral',
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)

        elif visualize == "Bar Chart":
            st.header("Top Users - Bar Chart")
            district_data = top_users_df_year.groupby('district')['district_users'].sum().reset_index()
            fig = px.bar(
                district_data,
                x='district',
                y='district_users',
                title=f'Total District Users by District ({selected_year})',
                labels={'district': 'District', 'district_users': 'District Users'},
                height=400
            )
            st.plotly_chart(fig)

        elif visualize == "Pie Chart":
            st.header("Top Users - Pie Chart")
            district_data = top_users_df_year.groupby('district')['district_users'].sum().reset_index()
            fig = px.pie(
                district_data,
                names='district',
                values='district_users',
                title=f'District Users Distribution by District ({selected_year})'
            )
            st.plotly_chart(fig)

# Drop downs
fact_option = st.sidebar.selectbox("Interesting Facts", [
    "Top State by Transaction Amount",
    "Most Common Transaction Type",
    "State with Highest Transaction Count",
    "Top Transaction Type by Amount",
    "Average Transaction Amount by State",
    "State with Most Unique Transaction Types",
    "Top District by Transaction Amount",
    "Top District by Registered Users",
    "Top 5 Pincodes by Transaction Amount",
    "Top 5 Brands by User Count"
])

# Interesting Facts
if fact_option == "Top State by Transaction Amount":
    st.header("Interesting Fact: Top State by Transaction Amount")
    state_amounts = agg_trans_df_year.groupby('state')['transaction_amount'].sum().reset_index()
    top_state = state_amounts.sort_values(by='transaction_amount', ascending=False).iloc[0]
    st.write(f"State: {top_state['state']}")
    st.write(f"Total Transaction Amount: {top_state['transaction_amount']:.2f}")

elif fact_option == "Most Common Transaction Type":
    st.header("Interesting Fact: Most Common Transaction Type")
    transaction_counts = agg_trans_df_year.groupby('transaction_type')['transaction_count'].sum().reset_index()
    most_common_type = transaction_counts.sort_values(by='transaction_count', ascending=False).iloc[0]
    st.write(f"Transaction Type: {most_common_type['transaction_type']}")
    st.write(f"Transaction Count: {most_common_type['transaction_count']}")

elif fact_option == "State with Highest Transaction Count":
    st.header("Interesting Fact: State with Highest Transaction Count")
    state_counts = agg_trans_df_year.groupby('state')['transaction_count'].sum().reset_index()
    highest_count_state = state_counts.sort_values(by='transaction_count', ascending=False).iloc[0]
    st.write(f"State: {highest_count_state['state']}")
    st.write(f"Transaction Count: {highest_count_state['transaction_count']}")

elif fact_option == "Top Transaction Type by Amount":
    st.header("Interesting Fact: Top Transaction Type by Amount")
    type_amounts = agg_trans_df_year.groupby('transaction_type')['transaction_amount'].sum().reset_index()
    top_transaction_type = type_amounts.sort_values(by='transaction_amount', ascending=False).iloc[0]
    st.write(f"Transaction Type: {top_transaction_type['transaction_type']}")
    st.write(f"Transaction Amount: {top_transaction_type['transaction_amount']:.2f}")

elif fact_option == "Average Transaction Amount by State":
    st.header("Interesting Fact: Average Transaction Amount by State")
    avg_amount = agg_trans_df_year.groupby('state')['transaction_amount'].mean().reset_index()
    avg_amount = avg_amount.rename(columns={'transaction_amount': 'average_amount'})
    st.write(avg_amount)

elif fact_option == "State with Most Unique Transaction Types":
    st.header("Interesting Fact: State with Most Unique Transaction Types")
    unique_types_per_state = agg_trans_df_year.groupby('state')['transaction_type'].nunique().reset_index()
    state_with_most_types = unique_types_per_state.sort_values(by='transaction_type', ascending=False).iloc[0]
    st.write(f"State: {state_with_most_types['state']}")
    st.write(f"Number of Unique Transaction Types: {state_with_most_types['transaction_type']}")

elif fact_option == "Top District by Transaction Amount":
    st.header("Interesting Fact: Top District by Transaction Amount")
    district_amounts = map_trans_df_year.groupby('district')['amount'].sum().reset_index()
    top_district = district_amounts.sort_values(by='amount', ascending=False).iloc[0]
    st.write(f"District: {top_district['district']}")
    st.write(f"Total Transaction Amount: {top_district['amount']:.2f}")

elif fact_option == "Top District by Registered Users":
    st.header("Interesting Fact: Top District by Registered Users")
    district_users = map_users_df_year.groupby('district')['registered_user'].sum().reset_index()
    top_district_users = district_users.sort_values(by='registered_user', ascending=False).iloc[0]
    st.write(f"District: {top_district_users['district']}")
    st.write(f"Registered Users: {top_district_users['registered_user']}")

elif fact_option == "Top 5 Pincodes by Transaction Amount":
    st.header("Interesting Fact: Top 5 Pincodes by Transaction Amount")
    top_pincodes = top_trans_df_year.groupby('pincode')['pincode_amount'].sum().reset_index()
    top_pincodes = top_pincodes.sort_values(by='pincode_amount', ascending=False).head(5)
    st.write(top_pincodes)

elif fact_option == "Top 5 Brands by User Count":
    st.header("Interesting Fact: Top 5 Brands by User Count")
    top_brands = agg_users_df_year.groupby('brands')['count'].sum().reset_index()
    top_brands = top_brands.sort_values(by='count', ascending=False).head(5)
    st.write(top_brands)