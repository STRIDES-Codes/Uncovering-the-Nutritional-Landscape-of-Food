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


def create_barcharts(df):
    keys = sorted(['Vitamin A', 'Vitamin B12',
                  'Vitamin D', 'Vitamin E', 'Vitamin K'], reverse=True)
    df = df.loc[df['Vitamin'].isin(keys)].sort_values(
        by=['Vitamin'], ascending=True)

    data = {}

    for row in df.itertuples(index=False):
        data.setdefault(row[1], {})
        data[row[1]].setdefault(
            row[3], row[4]
        )

    major_category = []
    for k in keys:
        major_category.extend([k] * (len(list(data.keys())) + 1))

    minor_category = []
    minor_category.extend((['Total'] + list(data.keys()))
                          * (len(keys)))

    y = [major_category, minor_category]
    print(y)

    fig = go.Figure(
    )

    for food_name in data:
        array = []
        for i in range(len(minor_category)):
            if minor_category[i] != 'Total' and minor_category[i] != food_name:
                array.append(0)
            else:
                array.append(data[food_name][major_category[i]])
        data[food_name]['bar_chart'] = array
        fig.add_bar(y=y, x=array, orientation='h', name=food_name,
                    text=array, textposition='auto')

    fig.update_layout(
        barmode='relative',
        title=dict(text='Breakdown of micronutrients'),
    )
    fig.update_xaxes(title=dict(text='Percentage of daily intake in decimal'))

    return st.plotly_chart(fig)


if options != []:
    selected = food.loc[food['Food_name'].isin(options)]
    st.write('You selected:', selected)
    create_barcharts(selected)
