import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(layout="wide")

# Title of the dashboard
st.title("Finance Data Analysis")

uploaded_file = st.file_uploader("Choose a file")

# Initialize dataframe as empty
dataframe = pd.DataFrame()

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(StringIO(bytes_data.decode("utf-8")), skiprows=1)
    st.write(dataframe.head())  # Commented this line to avoid displaying the full dataframe

    # Sidebar for selections
    st.sidebar.header("Selections")

    # Select Department (勘定科目)
    selected_account = st.sidebar.multiselect('Select Department (勘定科目):', dataframe['勘定科目'].dropna().unique().tolist())
    if selected_account:
        dataframe = dataframe[dataframe['勘定科目'].isin(selected_account)]

    # Select Department (部門)
    selected_division = st.sidebar.multiselect('Select Department (部門):', dataframe['部門'].dropna().unique().tolist())
    if selected_division:
        dataframe = dataframe[dataframe['部門'].isin(selected_division)]

    # Select Department (メモタグ)
    selected_memo_tag = st.sidebar.multiselect('Select Department (メモタグ):', dataframe['メモタグ'].dropna().unique().tolist())
    if selected_memo_tag:
        dataframe = dataframe[dataframe['メモタグ'].isin(selected_memo_tag)]


#import matplotlib.pyplot as plt
#import seaborn as sns

#plt.figure(figsize=(10, 6))
#sns.barplot(x='借方金額', y='勘定科目', data=dataframe) # 'value' should be replaced with the column you want to plot
#plt.title('Bar Plot by Department')
#st.pyplot(plt.gcf())

#勘定科目の（交際費、消耗品費、支払手数料、旅費交通費）に関連するメモタグのTOP 10をグラフ化
import plotly.express as px

if uploaded_file is not None:
    # Define the selected accounts
    selected_accounts = ['交際費', '消耗品費', '支払手数料', '旅費交通費']

    for i in range(0, len(selected_accounts), 2):
        # Create a column layout for each row
        cols = st.columns(2)

        for j in range(2):
            account = selected_accounts[i + j]
            # Filter data for the specific account
            filtered_data = dataframe[dataframe['勘定科目'] == account]

            # Check if the filtered data is not empty
            if not filtered_data.empty:
                # Group by 'メモタグ', and sum the '借方金額'
                grouped_data = filtered_data.groupby('メモタグ')['借方金額'].sum().reset_index()

                # Sort by '借方金額' and select top 10
                top_10_memo_tags = grouped_data.sort_values('借方金額', ascending=False).head(10)

                # Create a bar plot using Plotly Express
                fig = px.bar(top_10_memo_tags, x='メモタグ', y='借方金額', title=f'Top 10 メモタグ by {account}')

                # Update y-axis to show values in yen
                fig.update_layout(yaxis_title='借方金額 (円)', showlegend=False)
                fig.update_yaxes(tickprefix='¥', showgrid=True)

                # Show the plot in the corresponding column
                cols[j].plotly_chart(fig)
            else:
                cols[j].write(f"{account} is not found in the uploaded data.")






#勘定科目の（交際費、消耗品費、支払手数料、旅費交通費）に関連する部門のTOP 10をグラフ化
