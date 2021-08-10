import streamlit as st
import pandas as pd
import plotly.graph_objects as go

DATA_URL = 'https://raw.githubusercontent.com/STRIDES-Codes/Uncovering-the-Nutritional-Landscape-of-Food/main/foods_and_nutrients.tsv'

st.title('Uncovering the Nutritional Landscape of Food')


@st.cache
def load_data():
    df = pd.read_csv(DATA_URL, sep='\t')
    return df


food = load_data()
st.write(food)

################################################################################


options = st.multiselect(
    'Select Foods',
    food['Food_name'].unique(), ['Nuts, almonds']
)

if options != []:
    selected = food.loc[food['Food_name'].isin(options)]
    st.write('You selected:', selected)


def create_barcharts(df):
    keys = sorted(['Vitamin B12', 'Vitamin D'])
    df = df.loc[df['Vitamin'].isin(keys)].sort_values(
        by=['Vitamin'], ascending=True)

    print(df)

    data = {}

    for row in df.itertuples(index=False):
        data.setdefault(row[1], [])
        data[row[1]].append(
            (row[3], row[4])
        )

    bar = []
    for key in data:
        bar.append(go.Bar(name=key, y=keys, x=[
                   tuple[1] for tuple in data[key]], orientation='h'))

    fig = go.Figure(
        data=bar
    )
    fig.update_layout(barmode='stack')

    return st.plotly_chart(fig)


if options != []:
    create_barcharts(selected)
