import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache
def load_data():
    df = pd.read_csv(
        'https://api.covid19india.org/csv/latest/state_wise.csv'
    )
    return df
def print_pie(state_name:str):
    all_data = df[df['State']==state_name].T.reset_index().iloc[1:5]
    all_data.columns = ['column','cases']
    if state_name == 'Total':
        state_name='India'
    fig = px.pie(all_data, values='cases', names='column', title='Total Number of Cases in '+state_name)
    return fig

@st.cache
def get_map_by_cases(case_type:str):
    fig = go.Figure(data=go.Choropleth(
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locationmode='geojson-id',
        locations=df['State'],
        z=df[case_type],

        autocolorscale=False,
        colorscale='Reds',
        marker_line_color='peachpuff',

        colorbar=dict(
            title={'text': case_type+" Cases"},

            thickness=20,
            len=1,
            bgcolor='rgba(255,255,255,0.6)',

            tick0=0,
            dtick=300000,

            xanchor='left',
            x=0.01,
            yanchor='bottom',
            y=0.05
        )
    ))

    fig.update_geos(
        visible=False,
        projection=dict(
            type='conic conformal',
            parallels=[12.472944444, 35.172805555556],
            rotation={'lat': 24, 'lon': 80}
        ),
        lonaxis={'range': [68, 98]},
        lataxis={'range': [6, 38]}
    )

    fig.update_layout(
        title=dict(
            text=case_type+" COVID-19 Cases in India",
            xanchor='center',
            x=0.5,
            yref='paper',
            yanchor='bottom',
            y=1,
            pad={'b': 10}
        ),
        margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
        height=700,
        width=700
    )

    return fig
# Read in the cereal data
df = load_data()

st.title('COVID-19 INDIA VISUALIZATION')

st.subheader('Active Cases of India Bar Plot By State')
fig = px.bar(df.loc[1:36], x='State_code', y='Active',text='Active',labels={'Active':'Active Cases of India State','State_code':'Indian States Code'}, height=500,width=800)
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8)
st.plotly_chart(fig)

state_list = df.State[0:36].to_list()

st.subheader('COVID-19 TOTAL CASES BY ALL INDIA & STATE')
op = st.selectbox('Select State Name', state_list)
fig = print_pie(op)
st.plotly_chart(fig)

st.subheader('COVID-19 CASES MAP ALL INDIA')
case_list = ['Active','Confirmed','Recovered','Deaths']
opt = st.selectbox('Select Case', case_list)
fig = get_map_by_cases(opt)
st.plotly_chart(fig)

st.subheader("Covid Data for india by State")
st.table(df[['State', 'Confirmed', 'Recovered', 'Deaths', 'Active',
       'Last_Updated_Time']].sort_values(by='Active',ascending=False).reset_index(drop=True)[1:36])