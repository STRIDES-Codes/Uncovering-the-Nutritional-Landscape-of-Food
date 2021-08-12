import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

pd.set_option('display.max_columns', 5)

st.title("Understanding the Landscape of Nutrition")
st.sidebar.title("Options")
type = st.sidebar.selectbox(
    "Mode", ["Individual Foods", "Comparison", "Diet with Recommendations"])

col1, col2, col3 = st.columns(3)

with col1:
    sex = st.radio("What is your Biological Sex?", [
                   'Male 19-30y', 'Female 19-30y'])
with col2:
    diet = st.radio("Do you have any dietary limitations?", [
                    "None", "Vegetarian", "Vegan", "Ovolactarian"])
with col3:
    act = st.radio("What is your activitiy level?", [
                   "Sedentary", "Lightly Active", "Moderately Active", "Highly Active"])


d = pd.read_csv("data/nutrient_foodname_DRI.csv")


if sex == 'Male 19-30y':
    d.loc[:, "Percent_of_daily_intake"] = (
        (d.nutrient_value * d.DRI_conv) / d.DRI_MALE).round(3)
else:
    d.loc[:, "Percent_of_daily_intake"] = (
        (d.nutrient_value * d.DRI_conv) / d.DRI_FEM).round(3)

d = d.drop_duplicates(subset=["DRI_name", "food"])


dl = (d.pivot_table(index=["food"], columns=["DRI_name"], values="Percent_of_daily_intake")
      .reset_index())
colors = px.colors.qualitative.Pastel1
# st.write(dl)

if type == "Individual Foods":
    food = st.selectbox("Food", dl.food)

    cfp = dl.loc[dl.food == food, ["Carbohydrate", "Protein", "Total Fiber"]]
    cfp.loc[1, :] = [(1-i) for i in cfp.iloc[0, :]]
    vit = d.loc[(d.food == food) & (d.DRI_name.str.contains(
        "vita|fol|nia|flav|thia", case=False))].sort_values("DRI_name")
    min = d.loc[(d.food == food) & (d.DRI_name.str.contains(","))
                ].sort_values("DRI_name")
    # Create subplots, using 'domain' type for pie charts
    specs = [[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}],
             [{'colspan': 3}, None, None],
             [{'colspan': 3}, None, None]]
    fig = make_subplots(rows=3, cols=3, specs=specs, vertical_spacing=0.1,
                        subplot_titles=["Carbohydrates", "Proteins", "Fiber", "Vitamins", "Minerals"])

    # Define pie charts
    fig.add_trace(go.Pie(name="Carbs", labels=["Met", "Missing"], marker={
                  "colors": [colors[1], colors[-1]]}, values=cfp.Carbohydrate), 1, 1)
    fig.add_trace(go.Pie(name="Protein", labels=[
                  "Met", "Missing"], values=cfp.Protein), 1, 2)
    fig.add_trace(go.Pie(name="Fat", labels=[
                  "Met", "Missing"], values=cfp.loc[:, "Total Fiber"]), 1, 3)
    fig.add_trace(go.Bar(x=vit.DRI_name, y=vit.Percent_of_daily_intake *
                  100, marker={'color': colors[2]}), 2, 1)
    fig.add_trace(go.Bar(x=min.DRI_name, y=min.Percent_of_daily_intake *
                  100, marker={'color': colors[3]}), 3, 1)

    # Tune layout and hover info
    fig.update_yaxes(title_text='Percent Daily Value')
    fig.update_traces(hoverinfo='label+text+value', selector=dict(type='pie'))
    fig.update_traces(showlegend=False, selector=dict(type='bar'))

    fig.update_layout(height=1000)
    fig.update(layout_title_text='Essential Nutrients (per 100 g serving)',
               layout_title_font_size=24)

    st.plotly_chart(fig)


elif type == "Comparison":
    foods = st.multiselect(
        "Foods", dl.food, ["Nuts, almonds", "Blueberries, raw", "Kale, raw"])

    cfp = dl.loc[dl.food.isin(foods), ["Carbohydrate",
                                       "Protein", "Total Fiber"]].sum(axis=0).copy()
    vit = d.loc[(d.food.isin(foods)) & (d.DRI_name.str.contains(
        "vita|fol|nia|flav|thia", case=False))].sort_values("DRI_name")
    min = d.loc[(d.food.isin(foods)) & (
        d.DRI_name.str.contains(","))].sort_values("DRI_name")
    # Create subplots, using 'domain' type for pie charts
    specs = [[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}],
             [{'colspan': 3}, None, None],
             [{'colspan': 3}, None, None]]
    fig = make_subplots(rows=3, cols=3, specs=specs, vertical_spacing=0.1,
                        subplot_titles=["Carbohydrates", "Proteins", "Fiber", "Vitamins", "Minerals"])

    # Define pie charts
    fig.add_trace(go.Pie(name="Carbs", labels=["Met", "Missing"], marker={"colors": [
                  colors[1], colors[-1]]}, sort=False, showlegend=False, values=[cfp.Carbohydrate, (1-cfp.Carbohydrate)]), 1, 1)
    fig.add_trace(go.Pie(name="Protein", labels=[
                  "Met", "Missing"], sort=False, showlegend=False,  values=[cfp.Protein, (1-cfp.Protein)]), 1, 2)
    fig.add_trace(go.Pie(name="Fiber", labels=["Met", "Missing"], sort=False, showlegend=False, values=[
                  cfp.loc["Total Fiber"], (1-cfp.loc["Total Fiber"])]), 1, 3)

    i = 0
    for f in foods:
        fig.add_trace(go.Bar(x=vit.loc[vit.food == f, "DRI_name"], y=vit.loc[vit.food == f, "Percent_of_daily_intake"] * 100,
                             hovertext=f, name=f, legendgroup=f, marker={'color': colors[i]}), 2, 1)
        fig.add_trace(go.Bar(x=min.loc[min.food == f, "DRI_name"], y=min.loc[min.food == f, "Percent_of_daily_intake"] * 100,
                             hovertext=f, name=f, legendgroup=f, showlegend=False, marker={'color': colors[i]}), 3, 1)
        i = (i+1)

    # Tune layout and hover info
    fig.update_yaxes(title_text='Percent Daily Value')
    fig.update_traces(hoverinfo='label+text+value', selector=dict(type='pie'))
    fig.update_traces(selector=dict(type='bar'))
    fig.update_layout(height=1000, barmode="stack")
    fig.update(layout_title_text='Essential Nutrients (per 100 g serving)',
               layout_title_font_size=24)

    st.plotly_chart(fig)

elif type == "Diet with Recommendations":
    food = d.copy()
    with st.container():
        st.subheader('Compare food micronutrients using bar charts')

        # Create a multiselector widget titled 'Select Foods', populate it with all unique food names
        options = st.multiselect(
            'Select Foods',
            sorted(food['food'].unique()), []
        )

        # Create a two column container
        col1, col2 = st.columns(2)

        unique_minerals = food['DRI_name'].unique().tolist()
        notis = ["Carbohydrate", "Protein",
                 "Total Fiber", "Choline", "Total Water"]
        unique_minerals = [
            nutrient for nutrient in unique_minerals if nutrient not in notis]

        unique_minerals = [
            nutrient for nutrient in unique_minerals
            if 'Vitamin' not in nutrient and ':' not in nutrient and ', ' in nutrient]

        # First column contains the vitamin multiselector
        with col1:
            # Grab all unique micronutrients
            unique_nutrients = food['DRI_name'].unique().tolist()
            # Loop through each micronutrient and filter out those that do contain the word 'Vitamin' in it
            unique_nutrients = [
                nutrient for nutrient in unique_nutrients if nutrient not in notis]
            unique_nutrients = [
                nutrient for nutrient in unique_nutrients if nutrient not in unique_minerals]
            vitamins_keys = st.multiselect(
                'Select Vitamins',
                sorted(unique_nutrients), []
            )

        with col2:
            # Loop through each micronutrient and filter out those that are not minerals

            mineral_keys = st.multiselect(
                'Select Minerals',
                sorted(unique_minerals), []
            )

        # Create two checkboxes, of which its isChecked status is referenced by the variables
        # 'total_checkbox' & 'gender_checkbox'
        total_checkbox: bool = st.checkbox('Show total only')
        #
        # gender_radio = st.radio(
        #     'Gender:', options=['Male 19-30y', 'Female 19-30y'])
        gender_checkbox = sex == 'Male 19-30y'

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
                       row[7] * 100) if male else (row[3] * row[6] / row[8] * 100)

                if row[4] in data[row[2]]:
                    # If the micronutrient appears in more than one row,
                    # then it ignores it unless it contains 'added' in its name
                    if 'added' in row[0]:
                        data[row[2]].update(
                            {row[4]: data[row[2]][row[4]] + dri})
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
                text='Percentage of daily intake (%)'), rangemode='tozero')

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
                                     row[7] * 100) if male else (row[3] * row[6] / row[8] * 100)
                        else:
                            found = True
                            break

                if not found:
                    data[row[2]].append(
                        [row[4], (row[3] * row[6] /
                                  row[7] * 100) if male else (row[3] * row[6] / row[8] * 100)]
                    )

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
                text='Percentage of daily intake (%)'), rangemode='tozero')
            return st.plotly_chart(fig)

        if options != []:
            selected = food.loc[food['food'].isin(options)]
            # st.write(selected)
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

    with st.container():
        st.subheader('Recommendations')

        data = pd.read_csv(
            "https://raw.githubusercontent.com/STRIDES-Codes/Uncovering-the-Nutritional-Landscape-of-Food/main/nutrient_foodname_amount.tsv",
            sep="\t")

        def get_info(food):
            '''Return a DataFrame containing nutrient data of only the food passed in'''
            return data[data["food"] == food]

        def get_nutrient(food, nutrient):
            '''Return the specific nutrient amount for a particular food and nutrient of interest'''
            thisFood = get_info(food)

            nutInfo = thisFood[thisFood["nutrient"]
                               == nutrient]["nutrient_value"]

            if (len(nutInfo) == 0):
                return 0

            return float(nutInfo.values)

          # contains the array of selected foods ['Apple', ...]
        # new df containing info about only those foods above
        if options != []:
            new_selected = data.loc[data['food'].isin(options)]

            daily_rec = {
                'Vitamin A, RAE': 900,
                'Vitamin B-12': 2.4,
                'Vitamin B-6': 1.3,
                'Vitamin D (D2 + D3)': 15,
                'Vitamin E (alpha-tocopherol)': 15
            }

            def create_data(df, keys=['Vitamin A, RAE', 'Vitamin B-12', 'Vitamin B-6', 'Vitamin D (D2 + D3)',
                                      'Vitamin E (alpha-tocopherol)']):
                keys = sorted(keys, reverse=True)

                # Filter out the df rows that do not contain the correct micronutrient
                df = df.loc[df['nutrient'].isin(keys)].sort_values(
                    by=['nutrient'], ascending=True)
                data = {}

                # Create the data format for easier Plotly graphing
                # {
                #   'Food name': {
                #                   'Micronutrient#1': value1 * unit_conversion / daily recommended,
                #                    ...
                #                },
                # }
                for row in df.itertuples(index=False):
                    data.setdefault(row[2], {})

                    data[row[2]].setdefault(
                        row[0], row[3] / daily_rec[row[0]] * 100
                    )
                total_dict = {}
                for k in keys:
                    total_dict.setdefault(k, 0)
                    for food in data:
                        total_dict[k] += data[food][k]
                data['Total'] = total_dict
                return data

            data2 = create_data(
                new_selected)

            def rec_foods(nutrient, numRecs=3):
                '''Recommend a food to satisfy the missing nutritional need of argument nutrient'''
                possibleFoods = data[data["nutrient"] == nutrient]
                possibleFoods.sort_values(
                    by=["nutrient_value"], ascending=False, inplace=True)
                # display(possibleFoods)

                # If there's enough foods with this nutrient
                if numRecs <= possibleFoods.shape[0]:
                    return possibleFoods.iloc[:numRecs]["food"].values

                return possibleFoods.iloc[0]["food"]

            lackingNutrient = min(data2["Total"], key=data2["Total"].get)
            # Array of foods to recommend
            foodsToRec = rec_foods(lackingNutrient)

            i = 1
            for f in foodsToRec:
                st.write(str(i) + ".    " + f)
                i = i + 1
