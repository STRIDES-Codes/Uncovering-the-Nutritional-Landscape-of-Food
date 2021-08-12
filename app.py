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

# Create a bar chart container for logical separation
with st.container():
    st.subheader('Compare food micronutrients using bar charts')

    # Create a multiselector widget titled 'Select Foods', populate it with all unique food names
    options = st.multiselect(
        'Select Foods',
        sorted(food['food'].unique()), []
    )

    # Create a two column container
    col1, col2 = st.columns(2)

    # First column contains the vitamin multiselector
    with col1:
        # Grab all unique micronutrients
        unique_nutrients = food['DRI_name'].unique().tolist()
        # Loop through each micronutrient and filter out those that do contain the word 'Vitamin' in it
        unique_nutrients = [
            nutrient for nutrient in unique_nutrients if 'Vitamin' in nutrient]
        vitamins_keys = st.multiselect(
            'Select Vitamins',
            sorted(unique_nutrients), []
        )

    with col2:
        unique_minerals = food['DRI_name'].unique().tolist()

        # Loop through each micronutrient and filter out those that are not minerals
        unique_minerals = [
            nutrient for nutrient in unique_minerals
            if 'Vitamin' not in nutrient and ':' not in nutrient and ', ' in nutrient]
        mineral_keys = st.multiselect(
            'Select Minerals',
            sorted(unique_minerals), []
        )

    # Create two checkboxes, of which its isChecked status is referenced by the variables
    # 'total_checkbox' & 'gender_checkbox'
    total_checkbox: bool = st.checkbox('Show total only')
    gender_checkbox: bool = st.checkbox('Male')

    def create_barcharts(df, keys=[], male: bool = True):
        """
        Args:
            df - A pandas dataframe containing the dataset.\n
            keys - A list of micronutrients to compare with, must match the micronutrient found in the df.\n
            male - A boolean, if True calculates percent daily intake using recommendation for males, else calculates
            for females. \n

        Returns:
            A streamlit plotly bar chart object.
        """
        keys = sorted(keys, reverse=True)

        # Filter out the df rows that do not contain the correct micronutrient
        df = df.loc[df['DRI_name'].isin(keys)].sort_values(
            by=['DRI_name'], ascending=True)
        data = {}

        # Create the data format for easier Plotly graphing
        # {
        #   'Food name': {
        #                   'Micronutrient#1': value1 * unit_conversion / daily recommended,
        #                    ...
        #                },
        # }
        for row in df.itertuples(index=False):
            # row[2] = Food name
            # row[3] = nutrient_value
            # row[6] = Conversion factor
            # row[4] = DRI name (simplified nutrient name)
            data.setdefault(row[2], {})

            dri = (row[3] * row[6] /
                   row[7]) if male else (row[3] * row[6] / row[8])

            if row[4] in data[row[2]]:
                # If the micronutrient appears in more than one row,
                # then it ignores it unless it contains 'added' in its name
                if 'added' in row[0]:
                    data[row[2]].update({row[4]: data[row[2]][row[4]] + dri})
            data[row[2]].setdefault(
                row[4], dri
            )

        # The major categories are the name of Micronutrients
        major_category = []
        for k in keys:
            major_category.extend([k] * (len(list(data.keys())) + 1))

        # The minor categories are each food name, and 'total' to stack them up.
        minor_category = []
        minor_category.extend((['Total'] + list(data.keys()))
                              * (len(keys)))

        # Each major category must have a minor category and vice versa thus the array ends up looking like
        # [[Vit A, Vit A, Vita A, Vit B, B, B], [Total, Food1, Food2, Total, Food1, Food2]]
        y = [major_category, minor_category]

        # Create the Plotly empty graph object
        fig = go.Figure()

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
