import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

df = pd.read_csv('startup_funding_cleaned.csv')

def load_investor_details(investor):
    # Table 
    st.title(investor)
    df[df['Investors'].str.contains(investor)].sort_values(by ='Amount',ascending = False).head()[['Startup','Amount','City']]

    # plot 
    top_invetment =df[df['Investors'].str.contains(investor)].sort_values(by ='Amount',ascending = False).head()[['Startup','Amount','City']]
    fig,ax =plt.subplots()
    ax.bar(top_invetment['Startup'],top_invetment['Amount'])
    st.pyplot(fig)
 # Showing total amount invested by investor 
    total_investment=round(df[df['Investors']==investor]['Amount'].sum())
    st.metric('Total invetment',str(total_investment))

def load_startup_details(startup):
#     # Table 
#     st.title(investor)
#     df[df['Investors'].str.contains(investor)].sort_values(by ='Amount',ascending = False).head()[['Startup','Amount','City']]

#     # plot 
#     top_invetment =df[df['Investors'].str.contains(investor)].sort_values(by ='Amount',ascending = False).head()[['Startup','Amount','City']]
#     fig,ax =plt.subplots()
#     ax.bar(top_invetment['Startup'],top_invetment['Amount'])
#     st.pyplot(fig)
#  # Showing total amount invested by investor 
#     total_investment=round(df[df['Investors']==investor]['Amount'].sum())
#     st.metric('Total invetment',str(total_investment))
    st.title(startup)
    startup_df=  df[df['Startup']==startup]
    amount = startup_df['Amount'].sum()
    city =startup_df['City'].iloc[0]
    vertical=startup_df['Vertical'].iloc[0]
    funding_rounds = startup_df['InvestmentnType'].value_counts().iloc[0]
    top_investor = startup_df['Investors'].str.split(',').explode().value_counts().index[0]
    uniq_investors = startup_df['Investors'].str.split(',').explode().nunique()
    with st.container():
        col1,col2,col3 =st.columns([1,1,1])
        with col1:
            st.markdown('### City')
            st.metric('',city)
        with col2:
                st.markdown('### Vertical')
                st.metric('',vertical)
        with col3:
                st.markdown('### Total Investment')
                st.metric('',str(amount))

    st.write("\n")
    st.write("\n")
   
    with st.container():
        col1,col2,col3 =st.columns([1,1,1])
        with col1:
            st.markdown('### Total Funding Rounds')
            st.metric('',funding_rounds)
        with col2:
                st.markdown('### Top Investor')
                st.metric('',top_investor)
        with col3:
                st.markdown('### Unique Investors')
                st.metric('',str(uniq_investors))
                
    startup_df=  df[df['Startup']==startup]

    with st.container():
        col1,col2 =st.columns([1,1])
        with col1:
            st.markdown('### Latest Funding Rounds')
            st.metric ('', startup_df['InvestmentnType'].iloc[0])
        with col2:
            st.markdown('### Date')
            st.metric('',startup_df['Date'].iloc[0])
    # investor vs amount
    fig,ax =plt.subplots()
    ax.bar(startup_df['Investors'],startup_df['Amount']/100000)
    ax.set_ylabel('Amount in 100000 $')
    plt.xticks(rotation = 45)

    ##### Date vs Amount 
    st.pyplot(fig)
    fig,ax =plt.subplots()
    ax.scatter(startup_df['Date'],startup_df['Amount'])
    plt.xticks(rotation=45)
    st.pyplot(fig)



def load_overall_analysis():
    st.markdown('### Total Investment')
    ## metric with big fonts 
    st.metric('',str(round(df['Amount'].sum())))
    pie=df.groupby('City')['Amount'].sum().sort_values(ascending = False).head(10)
    vertical_series = df.groupby('Vertical')['Amount'].sum().sort_values(ascending = False).head(10)
    # top 10 vericals
    with st.container():
        col1,col2 =st.columns([1.5,2])
        with col1:
            st.markdown('### City Wise Distribution')
            fig,ax=plt.subplots()
            ax.pie(pie,labels=pie.index,autopct='%1.1f%%')
            st.pyplot(fig)
        with col2:
            st.markdown ('### Vertical wise distribution')
            fig,ax = plt.subplots()
            ax.pie(vertical_series,labels = vertical_series.index,autopct='%1.1f%%')
            st.pyplot(fig)


    with st.container():
        col1,col2 =st.columns([1,1])
        with col1:
            st.markdown('### Top 10 Funded Startups')
            max_funded_startup = df.groupby('Startup')['Amount'].sum().sort_values(ascending = False).head(10)
            fig,ax = plt.subplots()
            plt.xticks(rotation = 45)
            ax.bar(max_funded_startup.index,max_funded_startup)
            st.pyplot(fig)
        with col2:
            st.markdown('### Top 10 Investors')
            top_invetors = df.groupby('Investors')['Amount'].sum().sort_values(ascending = False).head(10)
            fig,ax = plt.subplots()
            ax.pie(top_invetors,labels = top_invetors.index,autopct='%1.1f%%')
            st.pyplot(fig)

st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Choose Analysis Type', ['Overall Analysis', 'Startup', 'Investor'])
if option=='Investor':
    st.sidebar.title('Investor Analysis')
    investor=st.sidebar.selectbox('Select Investor',df['Investors'].str.split(',').sum())
    btn=st.sidebar.button('Show Investor Details') 
    if btn:
        load_investor_details(investor)

elif option=='Overall Analysis':
    st.sidebar.title('Overall Analysis')
    btn=st.sidebar.button('Show Overall Analysis')
    if btn:
        load_overall_analysis()
else:
    st.sidebar.title('Startup Analysis')
    startup = st.sidebar.selectbox('Select Startup',df['Startup'].unique())
    btn = st.sidebar.button('Show Startup Details')
    if btn:
        load_startup_details(startup)
   

       


