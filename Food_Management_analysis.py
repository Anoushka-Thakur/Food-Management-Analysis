# Food Management Analysis Script
# Presented by Anoushka Thakur

# PROJECT SUMMARY 
# Food wastage is a significant issue, with many households and restaurants discarding 
# surplus food while numerous people struggle with food insecurity. This project aims to 
# develop a Local Food Wastage Management System, where: 
# ● Restaurants and individuals can list surplus food. 
# ● NGOs or individuals in need can claim the food. 

# SKILLS TAKEAWY 
# 1. ● Python 
# 2. ● SQL 
# 3. ● Streamlit 


# Project Goals
# 1. Create a Streamlit application for food providers to list surplus food.
# 2. Facilitate easy access for NGOs and individuals to claim available food.
# 3. Analyze food wastage patterns and propose solutions to minimize waste.

# GITHUB LINK : https://github.com/Anoushka-Thakur/Food-Management-Analysis


# This script loads food management data from CSV files, 
# processes it into an SQLite database, and performs various analyses to answer questions 
# about food providers, receivers, claims, and food listings.


#!/usr/bin/env python3
import sqlite3
import pandas as pd
import os

# Create the path for csv file to detect the environment

# Detect environment (local vs Streamlit Cloud)
if os.path.exists("receivers_claims.csv") and os.path.exists("providers_foodlisting.csv"):
    # Running on Streamlit Cloud (or if CSVs are in the same repo folder)
    receivers_claims = pd.read_csv("receivers_claims.csv")
    providers_foodlisting = pd.read_csv("providers_foodlisting.csv")
else:
    # Running locally on Windows
    receivers_claims = pd.read_csv(r"C:\Users\anous\Downloads\foodmanagement\receivers_claims.csv")
    providers_foodlisting = pd.read_csv(r"C:\Users\anous\Downloads\foodmanagement\providers_foodlisting.csv")

print("✅ Data loaded successfully")
print("Receivers Claims columns:", receivers_claims.columns.tolist())
print("Providers Foodlisting columns:", providers_foodlisting.columns.tolist())


# Name the path
DB_PATH = ('food_waste.db')
# Create SQLite database (or connect if it exists)
conn = sqlite3.connect(DB_PATH)

# Write DataFrames to SQLite tables
conn = sqlite3.connect(DB_PATH)
receivers_claims.to_sql('receivers_claims', conn, if_exists='replace', index=False)
providers_foodlisting.to_sql('providers_foodlisting', conn, if_exists='replace', index=False)
conn.close()


# Optional: verify tables
conn = sqlite3.connect(DB_PATH)
print(pd.read_sql_query("SELECT * FROM receivers_claims LIMIT 5", conn))
print(pd.read_sql_query("SELECT * FROM providers_foodlisting LIMIT 5", conn))

conn = sqlite3.connect(DB_PATH)
# LETS BEGIN WITH EDA

# Answering questions based on the data

# FOOD PROVIDERS AND RECEIVERS
# 1. How many food providers and receivers are there in each city?
print("--- Question 1: Total number of food providers and receivers are there in each city ---\n")
# Query to get the number of providers and receivers per city
query = """
SELECT City,
       COUNT(DISTINCT Provider_ID) AS num_providers,
       COUNT(DISTINCT Receiver_ID) AS num_receivers
FROM (
    SELECT City, Provider_ID, NULL AS Receiver_ID
    FROM providers_foodlisting
    UNION ALL
    SELECT City, NULL AS Provider_ID, Receiver_ID
    FROM receivers_claims
) AS combined
GROUP BY City;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Get total number of food providers
query = """
SELECT COUNT(DISTINCT Provider_ID) AS Total_Food_Providers
FROM providers_foodlisting
"""
total_providers = pd.read_sql_query(query, conn)
print("Total Food Providers:", total_providers)

# Get total number of food receivers
query = """
SELECT COUNT(DISTINCT Receiver_ID) AS Total_Food_Receivers
FROM receivers_claims
"""
total_receivers = pd.read_sql_query(query, conn)
print("Total Food Receivers:", total_receivers) 

# 2. What is the contact information of food providers in a specific city?
print("\n--- Question 2: Contact information of food providers in a specific city ---\n")
city = 'New Jessica'  # Example city
query = f"""
SELECT Provider_ID, Name, Contact
FROM providers_foodlisting
WHERE City = '{city}';
"""
result = pd.read_sql_query(query, conn)
print(result)

# 3. What is the most common food type offered by providers?
print("\n--- Question 3: Most common food type offered by providers ---\n")
query = """SELECT Food_Type, COUNT(*) AS count
FROM providers_foodlisting
GROUP BY Food_Type
ORDER BY count DESC
LIMIT 1;
"""
result = pd.read_sql_query(query, conn)
print(result)

# 4. Which receivers have claimed the most food?
print("\n--- Question 4: Which receivers have claimed the most food? ---\n")
most_claimed_receivers_query = """
SELECT T1.Receiver_ID, T1.Name, T1.City, COUNT(*) AS Claim_Count
FROM receivers_claims AS T1
GROUP BY T1.Receiver_ID, T1.Name, T1.City
ORDER BY Claim_Count DESC
LIMIT 1
"""
result = pd.read_sql_query(most_claimed_receivers_query, conn)
print(result)


# FOOD LISTINGS AND AVAILABILITY

# 5. What is the total quantity of food available from all providers?
print("\n--- Question 5: What is the total quantity of food available from all providers? ---\n")
total_food_quantity_query = """
SELECT SUM(Quantity) AS Total_Food_Quantity
FROM providers_foodlisting
"""
result = pd.read_sql_query(total_food_quantity_query, conn)
print(result)

# 6. Which city has the highest number of food listings?
print("\n--- Question 6: City with the highest number of food listings ---\n")
query = """
SELECT City, COUNT(*) AS num_listings
FROM providers_foodlisting
GROUP BY City
ORDER BY num_listings DESC
LIMIT 1;
"""
result = pd.read_sql_query(query, conn)
print(result)







# 7. what is the total sum of food listings by providers?
print("\n--- Question 7: Total sum of food listings by providers ---\n")
query = """SELECT COUNT(*) AS total_listings
FROM providers_foodlisting;"""
result = pd.read_sql_query(query, conn)
print(result)

# 8. What is the total sum of food claims by receivers?
print("\n--- Question 8: Total sum of food claims by receivers ---\n")
query = """SELECT COUNT(*) AS total_claims
FROM receivers_claims;"""
result = pd.read_sql_query(query, conn)
print(result)

# 9. What is the average number of food listings per provider?
print("\n--- Question 9: Average number of food listings per provider ---\n")
query = """
SELECT AVG(num_listings) AS avg_listings_per_provider
FROM (
    SELECT Provider_ID, COUNT(*) AS num_listings
    FROM providers_foodlisting
    GROUP BY Provider_ID
) AS provider_listings;
"""
result = pd.read_sql_query(query, conn)
print(result)

# 10. What are the most commonly available food types?
print("\n--- Question 10: What are the most commonly available food types? ---\n")
most_common_food_types_query = """
SELECT Food_Type, COUNT(*) AS Type_Count
FROM providers_foodlisting
GROUP BY Food_Type
ORDER BY Type_Count DESC;
"""
result = pd.read_sql_query(most_common_food_types_query, conn)
print(result)

# CLAIMS AND DISTRIBUTION

# 11. How many food claims have been made for each food item?
print("\n--- Question 11: How many food claims have been made for each food item? ---\n")
claims_per_food_item_query = """
SELECT Food_ID, COUNT(*) AS Claim_Count
FROM receivers_claims
GROUP BY Food_ID
"""
result = pd.read_sql_query(claims_per_food_item_query, conn)
print(result)

# 12. Which provider has the most successful claims?
print("\n--- Question 12: Provider with the most successful claims ---\n")
query = """SELECT pf.Provider_ID, pf.Name, COUNT(*) AS successful_claims
FROM providers_foodlisting pf
JOIN receivers_claims rc ON pf.Food_ID = rc.Food_ID
WHERE rc.Status = 'Completed'
GROUP BY pf.Provider_ID, pf.Name
ORDER BY successful_claims DESC
LIMIT 1;"""
result = pd.read_sql_query(query, conn)
print(result)



# 13. What is the most common food type claimed by receivers?
print("\n--- Question 13: Most common food type claimed by receivers ---\n")
query = """SELECT Food_Type, COUNT(*) AS count
FROM providers_foodlisting
JOIN receivers_claims ON providers_foodlisting.Food_ID = receivers_claims.Food_ID
GROUP BY Food_Type
ORDER BY count DESC
LIMIT 1;"""
result = pd.read_sql_query(query, conn)
print(result)

# 14. Which food item has the highest number of claims?
print("\n--- Question 14: Food item with the highest number of claims ---\n")
query = """SELECT Food_ID, COUNT(*) AS num_claims
FROM receivers_claims
GROUP BY Food_ID
ORDER BY num_claims DESC
LIMIT 1;"""
result = pd.read_sql_query(query, conn)
print(result)

# 15. What is the percentage of claims by status?
print("\n--- Question 15: Percentage of claims by status ---\n")
query = """
SELECT Status,
       COUNT(*) * 100.0 / (SELECT COUNT(*) FROM receivers_claims) AS percentage
FROM receivers_claims
GROUP BY Status;
"""
result = pd.read_sql_query(query, conn)
print(result)

# ANALYSIS AND INSIGHTS

# 16. What is the average quantity of claims per receiver?
print("\n--- Question 16: Average quantity of claims per receiver ---\n")
query = """SELECT Name, COUNT(*) AS total_claims, 
       COUNT(*) * 1.0 / (SELECT COUNT(DISTINCT Receiver_ID) FROM receivers_claims) AS avg_claims_per_receiver
FROM receivers_claims   
GROUP BY Name;"""
result = pd.read_sql_query(query, conn)
print(result)

# 17. What is the most common meal type claimed by receivers?
print("\n--- Question 17: Most common meal type claimed by receivers ---\n")
query = """
SELECT pf.Meal_Type, COUNT(*) AS num_claims
FROM providers_foodlisting pf
JOIN receivers_claims rc ON pf.Food_ID = rc.Food_ID
GROUP BY pf.Meal_Type
ORDER BY num_claims DESC
LIMIT 1;
"""
result = pd.read_sql_query(query, conn)
print(result)

# 18. What is the total quantity of food donated by each provider?
print("\n--- Question 18: What is the total quantity of food donated by each provider? ---\n")
total_food_donated_by_provider_query = """
SELECT T1.Provider_ID, SUM(T1.Quantity) AS Total_Food_Donated
FROM providers_foodlisting AS T1
INNER JOIN receivers_claims AS T2 ON T1.Food_ID = T2.Food_ID
WHERE T2.Status = 'Completed'
GROUP BY T1.Provider_ID
ORDER BY Total_Food_Donated DESC
LIMIT 10
"""
result = pd.read_sql_query(total_food_donated_by_provider_query, conn)
print(result)


# 19. What is the total number of meal types offered by providers?
print("\n--- Question 19: Total number of meal types offered by providers ---\n")
query = """SELECT COUNT(DISTINCT Meal_Type) AS total_meal_types
FROM providers_foodlisting;"""
result = pd.read_sql_query(query, conn)
print(result)



providers_foodlisting.columns = providers_foodlisting.columns.str.strip()

# Print columns to debug
print(receivers_claims.columns)
print(providers_foodlisting.columns)
conn.close()



# Application Development
#  Filter food donations based on location, provider, and food type. 
#  Contact food providers and receivers directly through the app. 
#  Implement CRUD operations for updating, adding, and removing records.
#  Implementing reminders and notifications for food providers and receivers.

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Custom CSS for background and text color
st.markdown(
    """
    <style>
    /* Set background color */
    .stApp {
        background-color: #black;
    }
    /* Change main text color */
    .stMarkdown, .stText, .stDataFrame, .stTable {
        color: #222831;
    }
    /* Change sidebar background and text */
    section[data-testid="stSidebar"] {
        background-color: #393e46;
        color: #3274c9;
    }
    /* Change header color */
    h1, h2, h3, h4 {
        color: #0077b6;
    }
    /* Change button color */
    .stButton>button {
        background-color: #00b4d8;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Custom CSS for title and headers
st.markdown(
    """
    <style>
    /* Change the color of the main title */
    .stApp h1 {
        color: #1426c9 !important;  /* Custom blue */
    }
    /* Change the color of h2 headers */
    .stApp h2 {
        color: #457b9d !important;  /* Example: blue */
    }
    /* Change the color of h3 headers */
    .stApp h3 {
        color: #2a9d8f !important;  /* Example: teal */
    }
    /* Change the color of Streamlit tabs (CRUD tabs) */
    div[data-testid="stTabs"] button {
        background-color: #3274c9 !important;
        color: #fff !important;
        border-radius: 8px 8px 0 0 !important;
        font-weight: bold;
        margin-right: 2px;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        background-color: #3274c9 !important;
        color: #fff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* Style for Add, Update, Delete buttons */
    .stButton > button {
        background-color: #00b894;
        color: white ;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        padding: 0.5em 2em;
        margin-bottom: 10px;
    }
    /* Style for form input fields */
    .stTextInput > div > input, .stNumberInput > div > input {
        background-color: #2a9d8f;
        color: #222831;
        border-radius: 6px;
        border: 1px solid #00b894;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Database path

DB_PATH = ('food_waste.db')

import sqlite3
def get_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    return conn

def run_query(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.title("Food Waste Management Dashboard") 

# KPI Section
st.header("Key Performance Indicators (KPIs)")
# Get KPI values from your database
total_providers = run_query("SELECT COUNT(DISTINCT Provider_ID) AS count FROM providers_foodlisting")['count'][0]
total_receivers = run_query("SELECT COUNT(DISTINCT Receiver_ID) AS count FROM receivers_claims")['count'][0]
total_listings = run_query("SELECT COUNT(*) AS count FROM providers_foodlisting")['count'][0]
total_claims = run_query("SELECT COUNT(*) AS count FROM receivers_claims")['count'][0]
total_food_available = run_query("SELECT SUM(Quantity) AS total FROM providers_foodlisting")['total'][0]
claims_completed = run_query("SELECT COUNT(*) AS count FROM receivers_claims WHERE Status='Completed'")['count'][0]
claims_completion_rate = (claims_completed / total_claims * 100) if total_claims else 0

def kpi_card(label, value):
    st.markdown(
        f"""
        <div style="background-color:#f0f4f8; padding:20px; border-radius:10px; text-align:center; margin-bottom:10px;">
            <span style="color:#030838; font-size:18px; font-weight:bold;">{label}</span><br>
            <span style="color:#030838; font-size:32px; font-weight:bold;">{value}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

col1, col2, col3 = st.columns(3)
with col1:
    kpi_card("Total Providers", total_providers)
    kpi_card("Total Receivers", total_receivers)
with col2:
    kpi_card("Total Listings", total_listings)
    kpi_card("Total Claims", total_claims)
with col3:
    kpi_card("Food Available", int(total_food_available) if total_food_available else 0)
    kpi_card("Claims Completion Rate", f"{claims_completion_rate:.1f}%")

def run_query(query, params=None):
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_unique_values(column, table):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT DISTINCT {column} FROM {table}", conn)
    conn.close()
    return df[column].dropna().tolist()

# Implementing reminders and notifications for food providers and receivers.

import datetime

# Example: Reminder logic
today = datetime.date.today()

# Dummy condition: If today is Monday, remind providers to update listings
if today.weekday() == 0:  
    st.warning("🔔 Reminder for Providers: Please update your food listings for the week!")

# Dummy condition: If claims exist but are pending
pending_claims = run_query("SELECT COUNT(*) as cnt FROM receivers_claims WHERE Status='Pending'")['cnt'][0]
if pending_claims > 0:
    st.info(f"🔔 Reminder for Receivers: You have {pending_claims} pending claims. Please follow up!")


# --- Sidebar Filters ---
st.sidebar.header("Filters")
city = st.sidebar.selectbox("City", ["All"] + get_unique_values("City", "providers_foodlisting"))
provider = st.sidebar.selectbox("Provider", ["All"] + get_unique_values("Name", "providers_foodlisting"))
food_type = st.sidebar.selectbox("Food Type", ["All"] + get_unique_values("Food_Type", "providers_foodlisting"))
meal_type = st.sidebar.selectbox("Meal Type", ["All"] + get_unique_values("Meal_Type", "providers_foodlisting"))

# --- Query Filters ---
filters = []
if city != "All":
    filters.append(f"City = '{city}'")
if provider != "All":
    filters.append(f"Name = '{provider}'")
if food_type != "All":
    filters.append(f"Food_Type = '{food_type}'")
if meal_type != "All":
    filters.append(f"Meal_Type = '{meal_type}'")
query_filters = " AND ".join(filters)
if query_filters:
    query_filters = "WHERE " + query_filters
# --- Data Display ---
st.header("Food Listings")
query = f"""
SELECT * FROM providers_foodlisting {query_filters}
"""
df = run_query(query)
if df.empty:
    st.warning("No food listings found with the selected filters.")
else:   
    st.dataframe(df)


# Provider Contact Details
st.subheader("Provider Contact Details")
provider_contact_query = f"""
SELECT Provider_ID, Name, City, Contact, Food_Type, Meal_Type
FROM providers_foodlisting {query_filters}
"""
provider_contacts = run_query(provider_contact_query)
if provider_contacts.empty:
    st.info("No providers found with the selected filters.")
else:
    st.dataframe(provider_contacts)

# Receiver Contact Details
st.subheader("Receiver Contact Details")
receiver_contact_query = f"""
SELECT Receiver_ID, Name, City, Contact, Status
FROM receivers_claims
{query_filters.replace('providers_foodlisting', 'receivers_claims') if query_filters else ''}
"""
receiver_contacts = run_query(receiver_contact_query)
if receiver_contacts.empty:
    st.info("No receivers found with the selected filters.")
else:
    st.dataframe(receiver_contacts)








# --- CRUD Operations ---
st.header("CRUD Operations")

crud_tab = st.tabs(["Add Provider", "Update Provider", "Delete Provider"],)

with crud_tab[0]:
    st.subheader("Add Provider")
    with st.form("add_provider"):
        name = st.text_input("Name")
        city = st.text_input("City")
        contact = st.text_input("Contact")
        food_type = st.text_input("Food Type")
        meal_type = st.text_input("Meal Type")
        quantity = st.number_input("Quantity", min_value=1)
        if st.form_submit_button("Add"):
            conn = get_connection()
            conn.execute(
                "INSERT INTO providers_foodlisting (Name, City, Contact, Food_Type, Meal_Type, Quantity) VALUES (?, ?, ?, ?, ?, ?)",
                (name, city, contact, food_type, meal_type, quantity)
            )
            conn.commit()
            conn.close()
            st.success("Provider added!")

with crud_tab[1]:
    st.subheader("Update Provider")
    df = run_query("SELECT * FROM providers_foodlisting")
    selected = st.selectbox("Select Provider to Update", df["Provider_ID"].tolist())
    if selected:
        row = df[df["Provider_ID"] == selected].iloc[0]
        with st.form("update_provider"):
            name = st.text_input("Name", row["Name"])
            city = st.text_input("City", row["City"])
            contact = st.text_input("Contact", row["Contact"])
            food_type = st.text_input("Food Type", row["Food_Type"])
            meal_type = st.text_input("Meal Type", row["Meal_Type"])
            quantity = st.number_input("Quantity", min_value=1, value=int(row["Quantity"]))
            if st.form_submit_button("Update"):
                conn = get_connection()
                conn.execute(
                    "UPDATE providers_foodlisting SET Name=?, City=?, Contact=?, Food_Type=?, Meal_Type=?, Quantity=? WHERE Provider_ID=?",
                    (name, city, contact, food_type, meal_type, quantity, selected)
                )
                conn.commit()
                conn.close()
                st.success("Provider updated!")

with crud_tab[2]:
    st.subheader("Delete Provider")
    df = run_query("SELECT * FROM providers_foodlisting")
    selected = st.selectbox("Select Provider to Delete", df["Provider_ID"].tolist())
    if st.button("Delete"):
        conn = get_connection()
        conn.execute("DELETE FROM providers_foodlisting WHERE Provider_ID=?", (selected,))
        conn.commit()
        conn.close()
        st.success("Provider deleted!")

# --- Visualize the data analysis with the help of charts ---
# Exapmple 1: The most frequent food providers and their contributions. 

st.header("1. Food Providers and Their Contributions")
query1 = """
SELECT Name, COUNT(*) AS num_listings, SUM(Quantity) AS total_contributed
FROM providers_foodlisting
GROUP BY Name
ORDER BY num_listings DESC, total_contributed DESC;
"""
df1 = run_query(query1)
st.dataframe(df1)
# Bar chart for food providers

st.subheader("Bar Chart: Food Providers Contributions")
st.bar_chart(df1.set_index('Name')['total_contributed'])

# Exampe 2: The highest demand locations based on food claims. 

st.header("2. Highest Demand Locations Based on Food Claims")
query2 = """
SELECT City, COUNT(*) AS total_claims
FROM receivers_claims
GROUP BY City
ORDER BY total_claims DESC;
"""
df2 = run_query(query2)
st.dataframe(df2)
st.bar_chart(df2.set_index('City')['total_claims'])


# Example 3: Food Types Distribution
st.header("3. Most Commonly Available Food Types")
query3 = """
SELECT Food_Type, COUNT(*) AS count
FROM providers_foodlisting
GROUP BY Food_Type
ORDER BY count DESC;
"""
df3 = run_query(query3)
st.dataframe(df3)

# Bar chart for food types
st.subheader("Bar Chart: Food Types Distribution")
st.bar_chart(df3.set_index('Food_Type'))

# Example 4: Meal Types Distribution
st.header("4. Most Common Meal Types")
query4 = """
SELECT Meal_Type, COUNT(*) AS count
FROM providers_foodlisting
GROUP BY Meal_Type  
ORDER BY count DESC;
""" 
df4 = run_query(query4)
st.dataframe(df4)
# Bar chart for meal types
st.subheader("Bar Chart: Meal Types Distribution")
st.bar_chart(df4.set_index('Meal_Type'))

# Example 5: Claims by Status

st.header("5. Claims by Status")
query5 = """
SELECT Status, COUNT(*) AS count
FROM receivers_claims
GROUP BY Status
ORDER BY count DESC;
"""
df5 = run_query(query5)
st.dataframe(df5)
# Bar chart for claims by status
st.subheader("Bar Chart: Claims by Status")
st.bar_chart(df5.set_index('Status'))

# Example 6: Claims by Type

st.header("6. Claims by Type")
query6 = """
SELECT Type, COUNT(*) AS count FROM receivers_claims GROUP BY Type ORDER BY count DESC;
"""
df6 = run_query(query6)
st.dataframe(df6)
# Bar chart for claims by type
st.subheader("Bar Chart: Claims by Type")
st.bar_chart(df6.set_index('Type'))

# Example 7: Claims by Food Type

st.header("7. Claims by Food Type")
query7 = """    
SELECT Food_Type, COUNT(*) AS count
FROM providers_foodlisting
JOIN receivers_claims ON providers_foodlisting.Food_ID = receivers_claims.Food_ID
GROUP BY Food_Type
ORDER BY count DESC;
""" 
df7 = run_query(query7)
st.dataframe(df7)
# Bar chart for claims by food type
st.subheader("Bar Chart: Claims by Food Type")
st.bar_chart(df7.set_index('Food_Type'))

# Example 8: Claims by Type

st.header("8. Claims by Type")
query8 = """
SELECT providers_foodlisting.Type, COUNT(*) AS count
FROM providers_foodlisting
JOIN receivers_claims ON providers_foodlisting.Food_ID = receivers_claims.Food_ID
GROUP BY providers_foodlisting.Type
ORDER BY count DESC;
"""
df8 = run_query(query8)
st.dataframe(df8)
# Bar chart for claims by type
st.subheader("Bar Chart: Claims by Type")
st.bar_chart(df8.set_index('Type'))

# Example 9: Claims by Provider

st.header("9. Claims by Provider")
query9 = """
SELECT pf.Provider_ID, pf.Name, COUNT(*) AS num_claims
FROM providers_foodlisting pf
JOIN receivers_claims rc ON pf.Food_ID = rc.Food_ID
GROUP BY pf.Provider_ID, pf.Name
ORDER BY num_claims DESC;
"""
df9 = run_query(query9)
st.dataframe(df9)
# Bar chart for claims by provider
st.subheader("Bar Chart: Claims by Provider")
st.bar_chart(df9.set_index('Name'))

# Example 10: Claims by Receiver

st.header("10. Claims by Receiver")
query10 = """
SELECT rc.Receiver_ID, rc.Name, COUNT(*) AS num_claims
FROM receivers_claims rc
GROUP BY rc.Receiver_ID, rc.Name
ORDER BY num_claims DESC;
"""
df10 = run_query(query10)
st.dataframe(df10)
# Bar chart for claims by receiver
st.subheader("Bar Chart: Claims by Receiver")
st.bar_chart(df10.set_index('Name'))

# Example 11: Claims by Food Item

st.header("11. Claims by Food Item")
query11 = """
SELECT Food_ID, COUNT(*) AS num_claims
FROM receivers_claims
GROUP BY Food_ID
ORDER BY num_claims DESC;
"""
df11 = run_query(query11)
st.dataframe(df11)
# Bar chart for claims by food item
st.subheader("Bar Chart: Claims by Food Item")
st.bar_chart(df11.set_index('Food_ID'))

# Example 12: Claims by Provider City

st.header("12. Claims by Provider City")
query12 = """
SELECT pf.City, COUNT(*) AS num_claims
FROM providers_foodlisting pf
JOIN receivers_claims rc ON pf.Food_ID = rc.Food_ID
GROUP BY pf.City
ORDER BY num_claims DESC;
"""
df12 = run_query(query12)
st.dataframe(df12)
# Bar chart for claims by provider city
st.subheader("Bar Chart: Claims by Provider City")
st.bar_chart(df12.set_index('City'))

# Example 13: Claims by Receiver City
st.header("13. Claims by Receiver City")
query13 = """
SELECT rc.City, COUNT(*) AS num_claims
FROM receivers_claims rc
GROUP BY rc.City
ORDER BY num_claims DESC;
""" 
df13 = run_query(query13)
st.dataframe(df13)
# Bar chart for claims by receiver city
st.subheader("Bar Chart: Claims by Receiver City")
st.bar_chart(df13.set_index('City'))

# Example 14: Claims by Provider Contact

st.header("14. Claims by Provider Contact")
query14 = """
SELECT pf.Contact, COUNT(*) AS num_claims
FROM providers_foodlisting pf
JOIN receivers_claims rc ON pf.Food_ID = rc.Food_ID

GROUP BY pf.Contact
ORDER BY num_claims DESC;
"""
df14 = run_query(query14)
st.dataframe(df14)
# Bar chart for claims by provider contact
st.subheader("Bar Chart: Claims by Provider Contact")
st.bar_chart(df14.set_index('Contact'))

# Example 15: Claims by Receiver Contact

st.header("15. Claims by Receiver Contact")
query15 = """
SELECT rc.Contact, COUNT(*) AS num_claims
FROM receivers_claims rc
GROUP BY rc.Contact 
ORDER BY num_claims DESC;
"""
df15 = run_query(query15)
st.dataframe(df15)
# Bar chart for claims by receiver contact
st.subheader("Bar Chart: Claims by Receiver Contact")
st.bar_chart(df15.set_index('Contact'))

# Example 16: Claims by Provider Food Type
st.header("16. Claims by Provider Food Type")

query16 = """
SELECT pf.Food_Type, COUNT(*) AS num_claims
FROM providers_foodlisting pf
JOIN receivers_claims rc ON pf.Food_ID = rc.Food_ID
GROUP BY pf.Food_Type
ORDER BY num_claims DESC;
""" 
df16 = run_query(query16)
st.dataframe(df16)
# Bar chart for claims by provider food type
st.subheader("Bar Chart: Claims by Provider Food Type")
st.bar_chart(df16.set_index('Food_Type'))


# Example 17: Claims by Provider Meal Type
st.header("17. Claims by Provider Meal Type")
query17 = """
SELECT pf.Meal_Type, COUNT(*) AS num_claims
FROM providers_foodlisting pf
JOIN receivers_claims rc ON pf.Food_ID = rc.Food_ID
GROUP BY pf.Meal_Type
ORDER BY num_claims DESC;
"""
df17 = run_query(query17)
st.dataframe(df17)
# Bar chart for claims by provider meal type
st.subheader("Bar Chart: Claims by Provider Meal Type")
st.bar_chart(df17.set_index('Meal_Type'))






# Conclusion

# Data Analysis Key Findings

# *   The data from the two CSV files were successfully loaded into SQLite tables named `providers_foodlisting` and `receivers_claims`.

# *   The total quantity of food available from all providers is 20000.

# *   Restaurants are the provider type that contributes the most food, with a total quantity of 5011.

# *   The city 'New Jessica' has the highest number of food listings (4).

# *   Dairy, Vegetables, and Meat are the most commonly available food types.

# *   Food item with ID 193 has the highest number of claims (11).

# *   Provider with ID 193 has the highest number of successful claims (11).

# *   Claim statuses are distributed relatively evenly: Completed (33.66%), Pending (33.33%), and Canceled (33.0%).

# *   Dinner is the most claimed meal type for completed claims (109).

# *   The average quantity of food claimed per receiver for completed claims is provided, with Receiver_ID 961 having an average of 11.0.

# SUGGESTIONS AND DECISION MAKING







