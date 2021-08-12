# Visualizing the Nutritional Landscape of Food: an NIH Codeathon

# Our Problem 
Dietary choices and nutrition behaviors are highly individual and change day to day. Many variables weigh heavily on a person's food choices:
- Access to food
- Work/school schedule
- Taste preference
- Culture

The decision of what foods to eat is further complicated by
- A person’s knowledge/understanding of diet and nutrition
- The Internet (media, online forums, etc.)
- Social media

All these factors make identifying factual and unbiased information regarding nutrition an increasingly difficult task.

*While it is largely difficult for scientific methods to account for all of the individual variations of diet preferences and access, information regarding nutritional content of food can be leveraged to develop data driven interpretations of foods.*

# Our Solution

Our primary aim for this project is to create an interactive visualization dashboard of a selection of foods and their nutritional contents (sourced from the United States Department of Agriculture (USDA) Food Data Central resource). 

# Visualization Dashboard

You can reach our Streamlit dashboard here:https://share.streamlit.io/tantar/uncovering-the-nutritional-landscape-of-food/main/UNLF.py. Currently we support three different types of visualizations for individual foods, comparison between foods, and the user's personal diet with recommendations.  

**Individual view:** If a user was interested in viewing the nutrition content for a single food item, they can select the Individual Foods option. Within this option, a food such as ocean perch can be evaluated for its carbohydrate, protein, and fiber content in comparison to USDA daily recommended intake, as well as a selection of nutrients including: Vitamins A, D, E, K, and C, B vitamins, calcium, copper, iron, magnesium, phosphorus, potassium, selenium, sodium, and zinc. An example of this visualization is shown below.

[![Screen-Shot-2021-08-12-at-12-38-43-PM.png](https://i.postimg.cc/Cx2TT1wk/Screen-Shot-2021-08-12-at-12-38-43-PM.png)](https://postimg.cc/Bj2w2JLn)
[![Screen-Shot-2021-08-12-at-12-38-49-PM.png](https://i.postimg.cc/dtQzhd1G/Screen-Shot-2021-08-12-at-12-38-49-PM.png)](https://postimg.cc/Lh7y7Jjs)

**Comparison view:** For users interested in viewing a nutrient comparison between multiple foods, the Comparison view allows for selection of various foods of interest and reports nutrient content. All nutrient options are consistent with those available in the Individual view, however this view is specifically color-coded to allow for consistent identification of what food item is contributing to each nutrient's daily recommended intake. This visualization can be seen here.

[![Screen-Shot-2021-08-12-at-12-42-44-PM.png](https://i.postimg.cc/J0pYN6nZ/Screen-Shot-2021-08-12-at-12-42-44-PM.png)](https://postimg.cc/7JTNDNSZ)
[![Screen-Shot-2021-08-12-at-12-42-52-PM.png](https://i.postimg.cc/HW66PNY7/Screen-Shot-2021-08-12-at-12-42-52-PM.png)](https://postimg.cc/bd20Z32z)

**Diet with Recommendations view:** This view is for individuals interested in gaining insight into how their current diet meets the daily recommended intake for each nutrient with recommendations on how to meet their daily needs. Within the Diet with Recommendations view users can select multiple foods and their nutrients of interest to receive visualization of that data. Additionally, in this view users will receive three recommended foods that are specifically selected to improve the nutrient content of the listed diet to meet dietary reference ranges. Dietary limitation and activity level information is not currently functional within this view.An example of this visualization is displayed below. 


[![Screen-Shot-2021-08-12-at-12-50-05-PM.png](https://i.postimg.cc/QdmgH9FK/Screen-Shot-2021-08-12-at-12-50-05-PM.png)](https://postimg.cc/bZGS5vHq)
[![Screen-Shot-2021-08-12-at-12-50-13-PM.png](https://i.postimg.cc/XJG9HsQ9/Screen-Shot-2021-08-12-at-12-50-13-PM.png)](https://postimg.cc/zbNL3Fmf)
[![Screen-Shot-2021-08-12-at-12-44-23-PM.png](https://i.postimg.cc/9z3RnVrh/Screen-Shot-2021-08-12-at-12-44-23-PM.png)](https://postimg.cc/9wpQD6d8)

All data on Dietary Reference Intakes are from the USDA (https://www.nal.usda.gov/sites/default/files/fnic_uploads/recommended_intakes_individuals.pdf) and are currently only applicable for individuals ages 19-30 years old. 


# For users of our Streamlit
This freely available dashboard only requires internet access. Any individual who is interested in using the dashboard is able to interact with it on their local machine.

# For those looking to replicate our Streamlit
First, an individual would need to download the datasets described in the "Datasets Used for this Project" section below. Once the foods and nutrient values are integrated into a single dataset, they would then need to calculate what percent of each nutrients recommended daily intakes it met by individual foods. If you are interested in skipping and using our aggregated dataset, it is made available in the data folder of our github. Individuals looking to replicate and edit the dashboard created for this project will need to download python and install the streamlit and plotly libraries. If interested in using our code, that is made readily available within our GitHub and can also be found in a condensed file on Zenodo. LINK

# Future Directions
We hope to continue refining our dashboard to include greater functionality and customization for users in a future codeathon. Our next steps for this project are to 1) increase the number of foods and nutrients our dashboard can reference, 2) automate updating of data from USDA FDC, 3) include macronutrients within the Diet + Recommendation view, 4) include all age bracket options for dietary reference intakes, 5) include activity level and dietary limitation specific customizations 6) allow for the serving size to be customized, and 7) pursue user testing and elicit feedback. 

# Datasets Used for this Project
- "Uncovering the Nutritional Landscape of Food by Kim" et al. [S1 Dataset. Foods analyzed in this study](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118697#references)

- [USDA FoodData Central](https://fdc.nal.usda.gov/download-datasets.html) [April 2019 (CSV – 6.1MB)](https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_sr_legacy_food_csv_%202019-04-02.zip)

# Our Team
Eric Ruan - Computer Science Undergrad at SBU

Eva Jason - Postbaccalaureate IRTA in the NICHD

Kyle Pu - Computer Science Undergrad at UCLA

Lauren Chan - PhD Candidate in Nutrition at Oregon State University

Tarek Antar - Postbaccalaurate IRTA in the NIA

Adam Thomas - NIMH

Dustin Moraczewski - NIMH

# References

Kim S, Sung J, Foo M, Jin Y-S, Kim P-J (2015) Uncovering the Nutritional Landscape of Food. PLoS ONE 10(3): e0118697. https://doi.org/10.1371/journal.pone.0118697

