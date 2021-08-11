import streamlit as st
import pandas as pd
import plotly.graph_objects as go

DATA_URL = 'https://raw.githubusercontent.com/STRIDES-Codes/Uncovering-the-Nutritional-Landscape-of-Food/main/nutrient_foodname_amount.tsv'

st.title('Uncovering the Nutritional Landscape of Food')


@st.cache
def load_data():
    df = pd.read_csv(DATA_URL, sep='\t')
    return df


food = load_data()

################################################################################

with st.container():
    st.subheader('Compare food micronutrients using bar charts')
    options = st.multiselect(
        'Select Foods',
        food['Food_Name'].unique(), ['Nuts, almonds']
    )

    col1, col2 = st.columns(2)

    with col1:
        vitamins_keys = st.multiselect(
            'Select Vitamins',
            ['Some', 'data', 'here'], ['data']
        )

    with col2:
        mineral_keys = st.multiselect(
            'Select Minerals',
            ['Some', 'data', 'here'], ['data']
        )

    st.checkbox('Show total')

    def create_barcharts(df, keys=['Vitamin A', 'Vitamin B12',
                                   'Vitamin D', 'Vitamin E', 'Vitamin K']):
        keys = sorted(keys, reverse=True)
        df = df.loc[df['name'].isin(keys)].sort_values(
            by=['name'], ascending=True)
        data = {}

        for row in df.itertuples(index=False):
            data.setdefault(row[6], {})
            data[row[6]].setdefault(
                row[3], row[1]
            )

        major_category = []
        for k in keys:
            major_category.extend([k] * (len(list(data.keys())) + 1))

        minor_category = []
        minor_category.extend((['Total'] + list(data.keys()))
                              * (len(keys)))

        y = [major_category, minor_category]

        fig = go.Figure(
        )

        for food_name in data:
            array = []
            for i in range(len(minor_category)):
                if minor_category[i] != 'Total' and minor_category[i] != food_name:
                    array.append(0)
                else:
                    try:
                        array.append(data[food_name][major_category[i]])
                    except KeyError:
                        data[food_name][major_category[i]] = 0
                        array.append(0)
            fig.add_bar(y=y, x=array, orientation='h', name=food_name,
                        text=array, textposition='auto')

        fig.update_layout(
            barmode='relative',
            title=dict(text='Breakdown of micronutrients'),
        )
        fig.update_xaxes(title=dict(
            text='Percentage of daily intake in decimal'), rangemode='tozero')

        return st.plotly_chart(fig)

    if options != []:
        selected = food.loc[food['Food_Name'].isin(options)]
        create_barcharts(
            selected, keys=['Vitamin D (D2 + D3)', 'Vitamin B-12'])
