import pandas as pd
import numpy as np
import streamlit as st

pd.set_option('display.max_columns', 5)

d = pd.read_csv("data/nutrient_foodname_amount.tsv", sep = "\t")

d.loc[:,"DRI_name"] = [np.nan if pd.isnull(i)
                       else "Carbohydrate" if i in ["Carbohydrate, by difference"]
                       else "Total Water" if i in ["Water"]
                       else "Total Fiber" if i in ["Fiber, total dietary"]
                       else "Vitamin A" if i in ["Retinol", "Vitamin A, RAE", "Vitamin A, IU"]
                       else "Vitamin C" if i in ["Vitamin C, total ascorbic acid"]
                       else "Vitamin D" if i in ["Vitamin D (D2 + D3), International Units", "Vitamin D (D2 + D3)",
                                                 "Vitamin D3 (cholecalciferol)","Vitamin D2 (ergocalciferol)"]
                       else "Vitamin E" if i in ["Tocopherol, delta","Tocotrienol, gamma","Tocotrienol, delta",
                                                 "Tocopherol, beta","Tocopherol, gamma","Tocotrienol, alpha",
                                                 "Tocotrienol, beta","Vitamin E (alpha-tocopherol)","Vitamin E, added"]
                       else "Choline" if i in ["Choline, total"]
                       else "Folate" if i in ["Folate, total","Folate, food","Folic acid","Folate, DFE"]
                       else "Vitamin B-12" if i in ["Vitamin B-12", "Vitamin B-12, added"]
                       else "Vitamin K" if i in ["Vitamin K (Dihydrophylloquinone)", "Vitamin K (phylloquinone)",
                                                 "Vitamin K (Menaquinone-4)"]
                       else i if i in ["Protein","Thiamin", "Riboflavin","Niacin","Vitamin B-6","Pantothenic acid",
                                       "Calcium, Ca","Copper, Cu","Iron, Fe","Magnesium, Mg","Phosphorus, P",
                                       "Selenium, Se","Zinc, Zn","Potassium, K","Sodium, Na",
                                       "Fluoride, F","Manganese, Mn"]
                       else np.nan for i in d.nutrient]

d = d[d.DRI_name.notna()]



d.loc[:,"DRI_unit"] = ["G" if i in ["Carbohydrate", "Protein", "Total Fiber","Potassium, K","Sodium, Na", "Chloride, Cl"]
                       else "MG" if i in ["Vitamin C","Vitamin E","Thiamin","Riboflavin","Niacin","Vitamin B-6",
                                          "Calcium, Ca","Iron, Fe","Magnesium, Mg","Phosphorus, P","Zinc, Zn",
                                          "Fluoride, F","Manganese, Mn","Pantothenic acid","Choline"]
                       else "UG" if i in ["Vitamin A","Vitamin D","Folate","Vitamin B-12","Vitamin K","Copper, Cu",
                                          "Selenium, Se"]
                       else "L" if i == "Total Water"
                       else np.nan for i in d.DRI_name]

d.loc[:,"DRI_conv"] = [1 if i == j
                            else 0.001 if ((i == "G") & (j == "L"))
                            else 0.001 if ((i == "MG") & (j == "G"))
                            else 0.001 if ((i == "UG") & (j == "MG"))
                            else 1000 if ((i == "MG") & (j == "UG"))
                            else 0.025 if k == "Vitamin D"
                            else 0.3 if k == "Vitamin A"
                            else np.nan for i,j,k in zip(d.unit,d.DRI_unit,d.DRI_name)]

d.loc[:,"DRI_MALE"] = [130 if i == "Carbohydrate"
                        else 56 if i == "Protein"
                        else 3.7 if i == "Total Water"
                        else 38 if i == "Total Fiber"
                        else 900 if i in ["Vitamin A","Copper, Cu"]
                        else 90 if i == "Vitamin C"
                        else 15 if i in ["Vitamin D","Vitamin E"]
                        else 1.2 if i == "Thiamin"
                        else 1.3 if i == "Riboflavin"
                        else 16 if i == "Niacin"
                        else 1.3 if i == "Vitamin B-6"
                        else 400 if i == "Folate"
                        else 2.4 if i == "Vitamin B-12"
                        else 5 if i == "Pantothenic acid"
                        else 120 if i == "Vitamin K"
                        else 1000 if i == "Calcium, Ca"
                        else 8 if i == "Iron, Fe"
                        else 400 if i == "Magnesium, Mg"
                        else 700 if i == "Phosphorus, P"
                        else 55 if i == "Selenium, Se"
                        else 11 if i == "Zinc, Zn"
                        else 550 if i == "Choline"
                        else 4.7 if i == "Potassium, K"
                        else 1.5 if i == "Sodium, Na"
                        else 2.3 if i == "Chloride, Cl"
                        else 4 if i == "Fluoride, F"
                        else 2.3 if i == "Manganese, Mn"
                        else np.nan for i in d.DRI_name]


d.loc[:,"DRI_FEM"] = [130 if i == "Carbohydrate"
                        else 4.6 if i == "Protein"
                        else 2.7 if i == "Total Water"
                        else 25 if i == "Total Fiber"
                        else 700 if i in ["Vitamin A","Copper, Cu"]
                        else 75 if i == "Vitamin C"
                        else 15 if i in ["Vitamin D","Vitamin E"]
                        else 1.1 if i in ["Thiamin","Riboflavin"]
                        else 14 if i == "Niacin"
                        else 1.3 if i == "Vitamin B-6"
                        else 400 if i == "Folate"
                        else 2.4 if i == "Vitamin B-12"
                        else 5 if i == "Pantothenic acid"
                        else 90 if i == "Vitamin K"
                        else 1000 if i == "Calcium, Ca"
                        else 18 if i == "Iron, Fe"
                        else 310 if i == "Magnesium, Mg"
                        else 700 if i == "Phosphorus, P"
                        else 55 if i == "Selenium, Se"
                        else 8 if i == "Zinc, Zn"
                        else 425 if i == "Choline"
                        else 4.7 if i == "Potassium, K"
                        else 1.5 if i == "Sodium, Na"
                        else 2.3 if i == "Chloride, Cl"
                        else 4 if i == "Fluoride, F"
                        else 1.8 if i == "Manganese, Mn"
                        else np.nan for i in d.DRI_name]

d.to_csv("data/nutrient_foodname_DRI.csv", index=False)