library(dplyr)
library(tidyr)
library(readxl)

nutrient <- read.csv("FoodData_Central_csv_2021-04-28/nutrient.csv",
                     na.strings = "") %>%
  select(name, unit_name, nutrient_nbr)
colnames(nutrient) <- c("nutrient",
                        "unit",
                        "nutrient_code")

nutrient$nutrient_code <- as.numeric(nutrient$nutrient_code)
nutrient <- filter(nutrient, !is.na(nutrient_code))

foods <- read.table("FoodData_Central_csv_2021-04-28/fndds_ingredient_nutrient_value.csv",
                    sep = ",",
                    header = TRUE) %>%
  select(SR.description, Nutrient.code, Nutrient.value)
colnames(foods) <- c("food", "nutrient_code", "nutrient_value")
foods$nutrient_code <- as.numeric(foods$nutrient_code)

nutrient_and_food <- left_join(nutrient, foods) %>%
  filter(!is.na(food)) %>%
  select(-nutrient_code)
groups <- read_excel("pone.0118697.s002.xlsx", skip = 1)
colnames(groups) <- c(
  "food_category",
  "belong_to_clusters",
  "food_cluster",
  "USDA_food_ID",
  "food",
  "nutritional_fitness",
  "price_USD_per_100g"
)

groups <- fill(groups, food_category, belong_to_clusters, food_cluster)

a <- left_join(nutrient_and_food, groups) %>%
  select(-USDA_food_ID)

write.table(a, file = "nutrient_food_unit_value_categories.tsv",
            sep = "\t",
            row.names = FALSE,
            quote = FALSE)