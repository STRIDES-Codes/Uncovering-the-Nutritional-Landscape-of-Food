# Visualizing the Nutritional Landscape of Food: an NIH Codeathon
# links to any resulting DOI


# Problem
Dietary choices and nutrition behaviors are highly individual and change day to day. Many variables weigh heavily on a person's food choices:
- Access to food
- Work/school schedule
- Taste preference
- Culture

The decision of what foods to eat is further complicated by
- A person’s knowledge/understanding of diet and nutrition
- The Internet (media, online forums, etc.)
- Social media

All these factors make idenfitfying factual and unbiased information regarding nutrition an increasingly difficult task.

*While it is largely difficult for scientific methods to account for all of the individual variations of diet preferences and access, information regarding nutritional content of food can be leveraged to develop data driven interpretations of foods.*

# Our Solution

Our primary aim for this project is to create an interactive visualization dashboard of a selection of foods and their nutritional contents (sourced from the United States Department of Agriculture (USDA) Food Data Central resource). 

# Visualization platform

You can reach our Streamlit dashboard here:https://share.streamlit.io/tantar/uncovering-the-nutritional-landscape-of-food/main/UNLF.py and experiment with Individual, Comparison, and Diet views. 

Individual view: If a user was interested in viewing the nutrition content for a single food item, they can select the Individual Food option. Within this option, a food such as ocean perch can be evaluated for its carbohydrate, protein, and fiber content in comparison to USDA DRIs as well as a selection of nutrients including: Vitamins A, D, E, K, and C, B vitamins, calcium, copper, iron, magnesium, phosphorus, potassium, selenium, sodium, zinc, choline, and total water. An example of this visualization is shown below.

Comparison view: For users interested in viewing a nutrient comparison between multiple foods, the Diet view allows for selection of various foods of interest and reports nutrient content. All nutrient options are consistent with those available in the Individual view. This view is specifically color-coded to allow for consistent identification of what food item is contributing what nutrient content. This visualization can be seen here.

Diet + Recommendation view: This view is for individuals interested in eliciting feedback regarding suggested foods to consume given a current dietary intake. Within the Diet with Recommendations view users can  select multiple foods and will receive the resulting nutrition content of each food. Additionally, in this view users will receive three recommended foods that are specifically selected to improve the nutrient content of the listed diet to meet dietary reference ranges. 

All data on Dietary Reference Intakes are from the USDA (https://www.nal.usda.gov/sites/default/files/fnic_uploads/recommended_intakes_individuals.pdf) and are currently only applicable for individuals ages 19-30 years old. 


# information for streamlit user
- include information about what the inputs are and what the outputs are (figure/ workflow diagram), describe them distinctly
- use some of the screenshot pieces here if possible from our use case

# information for those looking to replicate
- instructions for what to install, any dependencies, any example code we may be able to include

# planned features/ what's next
We hope to continue refining our dashboard to include greater functionality and customization for users in a future codeathon. Our next steps for this project are to 1) increase the number of foods and nutrients our dashboard can reference, 2) automate file ingestion, 3) include all age bracket options for dietary reference intakes, and 4) pursue user testing and elicit feedback. 

# datasets used

- "Uncovering the Nutritional Landscape of Food by Kim" et al. [S1 Dataset. Foods analyzed in this study](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118697#references)

- [USDA FoodData Central](https://fdc.nal.usda.gov/download-datasets.html) [April 2019 (CSV – 6.1MB)](https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_sr_legacy_food_csv_%202019-04-02.zip)

# Our Team
Eric Ruan

Eva Jason - Postbaccalaureate IRTA in the NICHD

Kyle Pu

Lauren Chan - PhD Candidate in Nutrition at Oregon State University

Tarek Antar

Adam Thomas

Dustin Moraczewski

# References

Kim S, Sung J, Foo M, Jin Y-S, Kim P-J (2015) Uncovering the Nutritional Landscape of Food. PLoS ONE 10(3): e0118697. https://doi.org/10.1371/journal.pone.0118697

