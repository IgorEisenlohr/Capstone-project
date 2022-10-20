import streamlit as st
import pandas as pd
import plotly.express as px

spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
spacex_df = spacex_df.rename(columns={'Payload Mass (kg)':"PayloadMass"})

def app_layout():
    st.title("SpaceX Launch Records Dashboard")
    option = st.selectbox("Launch Sites", options = ['All','CCAFS LC-40', 'VAFB SLC-4E', 'KSC LC-39A', 'CCAFS SLC-40'], key='selectbox')
       
    if option == 'All':
        launchsite_success = spacex_df.groupby('Launch Site')[['class']].count().reset_index()
        launchsite_success.columns = ['Launch Site', 'count']
        fig = px.pie(launchsite_success, values='count', names='Launch Site',title='Total Success By Site')
        fig.update_layout(font_size=20)
        st.plotly_chart(fig)
        
    else:
        #filtro do dataset de acordo com a opção escolhida
        specific_site_succes = spacex_df[spacex_df['Launch Site'] == option].groupby('class')[['Launch Site']].count().reset_index()  
        specific_site_succes.columns = ['class', 'count']
        #gerando o grafico em pizza para sucesso individual
        fig2 = px.pie(specific_site_succes, values='count', names='class', title=f'{option} Site success')
        
        fig2.update_layout(font_size=20 )
        #disponibilizando o gráfico
        st.plotly_chart(fig2)
        
    #alternado nome da coluna Payload Mass (kg) para facilitar na manipulação da variável
    min_slider, max_slider = st.slider(label='Payload range (kg)',value=(0,10000), step=1000)
    slider_df = spacex_df.query(f'PayloadMass > {min_slider} and PayloadMass < {max_slider}')
    
    if option == 'All':
        fig3 = px.scatter(slider_df, x='PayloadMass', y='class', color='Booster Version Category')
        st.plotly_chart(fig3)
        
    else:
        fig3 = px.scatter(slider_df, x='PayloadMass', y='class', color='Booster Version Category')
        st.plotly_chart(fig3)        
        
if __name__=='__main__':
    app_layout()
