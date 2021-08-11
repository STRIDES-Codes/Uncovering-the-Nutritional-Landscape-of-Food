import streamlit as st
import pandas as pd
import plotly.graph_objects as go


DATA_URL = 'https://raw.githubusercontent.com/STRIDES-Codes/Uncovering-the-Nutritional-Landscape-of-Food/main/nutrient_foodname_DRI.csv'

st.title('Uncovering the Nutritional Landscape of Food')


@st.cache
def load_data():
    df = pd.read_csv(DATA_URL, sep=',')
    df = df.astype({'unit': 'string', 'food': 'string',
                    'nutrient_value': 'float64'})
    return df


food = load_data()

################################################################################

with st.container():
    st.subheader('Compare food micronutrients using bar charts')
    options = st.multiselect(
        'Select Foods',
        sorted(food['food'].unique()), []
    )

    col1, col2 = st.columns(2)

    with col1:
        unique_nutrients = food['DRI_name'].unique().tolist()
        unique_nutrients = [
            nutrient for nutrient in unique_nutrients if 'Vitamin' in nutrient]
        vitamins_keys = st.multiselect(
            'Select Vitamins',
            sorted(unique_nutrients), []
        )

    with col2:
        unique_minerals = food['DRI_name'].unique().tolist()
        unique_minerals = [
            nutrient for nutrient in unique_minerals if 'Vitamin' not in nutrient and ':' not in nutrient and ', ' in nutrient]
        mineral_keys = st.multiselect(
            'Select Minerals',
            sorted(unique_minerals), []
        )

    total_checkbox = st.checkbox('Show total only')
    gender_checkbox = st.checkbox('Male')

    def create_barcharts(df, keys=[], male=True):
        keys = sorted(keys, reverse=True)
        df = df.loc[df['DRI_name'].isin(keys)].sort_values(
            by=['DRI_name'], ascending=True)
        data = {}

        for row in df.itertuples(index=False):
            data.setdefault(row[2], {})

            dri = (row[3] * row[6] /
                   row[7]) if male else (row[3] * row[6] / row[8])

            if row[4] in data[row[2]]:
                if 'added' in row[0]:
                    data[row[2]].update({row[4]: data[row[2]][row[4]] + dri})
            data[row[2]].setdefault(
                row[4], dri
            )

        # row[2] = Food name
        # row[3] = nutrient_value
        # row[6] = Conversion factor
        # row[4] = DRI name (simplified nutrient name)

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
                        text=array, textposition='auto', texttemplate='%{text:.2f}')

        fig.update_layout(
            barmode='relative',
            title=dict(text='Breakdown of Micronutrients'),
        )
        fig.update_xaxes(title=dict(
            text='Percentage of daily intake in decimal'), rangemode='tozero')

        return st.plotly_chart(fig)

    def create_barchartsStacked(df, keys=[], male=True):
        keys = sorted(keys, reverse=False)
        df = df.loc[df['DRI_name'].isin(keys)].sort_values(
            by=['DRI_name'], ascending=True)

        data = {}

        for row in df.itertuples(index=False):
            data.setdefault(row[2], [])

            found = False

            for x in data[row[2]]:
                if row[4] in x:
                    if 'added' in row[0]:
                        x[1] += (row[3] * row[6] /
                                 row[7]) if male else (row[3] * row[6] / row[8])
                    else:
                        found = True
                        break

            if not found:
                data[row[2]].append(
                    [row[4], (row[3] * row[6] /
                              row[7]) if male else (row[3] * row[6] / row[8])]
                )

        print(data)

        bar = []
        for key in data:
            bar.append(go.Bar(name=key, x=keys, y=[
                tuple[1] for tuple in data[key]], orientation='v'))

        fig = go.Figure(
            data=bar
        )
        fig.update_layout(
            barmode='stack',
            title=dict(text='Breakdown of Micronutrients'),
        )
        fig.update_xaxes(title=dict(
            text='Micronutrients'))
        fig.update_yaxes(title=dict(
            text='Percentage of daily intake in decimal'), rangemode='tozero')
        return st.plotly_chart(fig)

    if options != []:
        selected = food.loc[food['food'].isin(options)]
        st.write(selected)
        if vitamins_keys != []:
            if total_checkbox:
                create_barchartsStacked(
                    selected, keys=vitamins_keys, male=gender_checkbox)
            else:
                create_barcharts(selected, keys=vitamins_keys,
                                 male=gender_checkbox)

        if mineral_keys != []:
            if total_checkbox:
                create_barchartsStacked(
                    selected, keys=mineral_keys, male=gender_checkbox)
            else:
                create_barcharts(selected, keys=mineral_keys,
                                 male=gender_checkbox)

        if mineral_keys == [] and vitamins_keys == []:
            st.write('Please select micronutrient(s)')
