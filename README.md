# Customer Shopping Behaviour Dashboard

An interactive BI-style analytics dashboard built with Python and Streamlit, 
visualizing customer shopping patterns across 3,900 customers and 18 features.

**Live Demo:** [Click here](https://customer-behaviouranalysis.streamlit.app/)

---

## Dashboard Overview

- **KPI Cards** — Total revenue, average purchase, average rating, subscriber %
- **Revenue by Category** — Breakdown across Clothing, Accessories, Footwear, Outerwear
- **Top 10 Items Purchased** — Best selling products by units sold
- **Revenue by Season** — Seasonal purchasing trends
- **Payment Method Breakdown** — Distribution across PayPal, Credit Card, Cash, and more
- **Purchase Amount by Age Group & Gender** — Comparative spending across demographics
- **Subscribers vs Non-Subscribers** — Behavioural comparison across key metrics
- **Purchase Amount Distribution** — Box plot by category showing spread and outliers
- **Top 10 Locations by Revenue** — Highest revenue generating states

---

## Interactive Filters

All charts update dynamically based on sidebar filters:
- Season, Gender, Category, Subscription Status, Age Range

---

## Tech Stack

| Layer        | Tools                        |
|--------------|------------------------------|
| Data         | pandas, NumPy                |
| Visualisation| Plotly                       |
| Frontend     | Streamlit                    |
| Deployment   | Hugging Face Spaces          |

---

## Dataset

- **3,900** customer records
- **18 features** including age, gender, category, purchase amount, season, payment method, subscription status, and more
- Cleaned and feature engineered: age groups, purchase frequency in days, redundant columns removed

---

## Run Locally

```bash
git clone https://github.com/karan-cheemalapati/Customer-Shopping-Behaviour.git
cd Customer-Shopping-Behaviour
pip install -r requirements.txt
streamlit run dashboard.py
```

---

## Project Structure
```
├── dashboard.py                     # Streamlit dashboard app
├── Customer_Behaviour.ipynb         # Data cleaning & EDA notebook
├── customer_shopping_behavior.csv   # Raw dataset
├── customer_behaviour_cleaned.csv   # Cleaned dataset
└── requirements.txt
```
---

## Future Improvements

- Add RFM (Recency, Frequency, Monetary) customer segmentation
- Integrate clustering (K-Means) to identify customer personas
- Add time-series analysis if date data becomes available
- Export filtered data as CSV from the dashboard
