import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Customer Shopping Behaviour",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

        html, body, .stApp {
            background-color: #0e0e0e;
            color: #f0f0f0;
            font-family: 'DM Sans', sans-serif;
        }
        .stApp { background-color: #0e0e0e; }
        section[data-testid="stSidebar"] {
            background-color: #141414;
            border-right: 1px solid #2a2a2a;
        }
        .metric-card {
            background: linear-gradient(135deg, #1a1a1a, #1f1f1f);
            border: 1px solid #2a2a2a;
            border-radius: 16px;
            padding: 1.4rem 1.6rem;
            margin-bottom: 1rem;
        }
        .metric-label {
            font-size: 0.75rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #888;
            margin-bottom: 0.4rem;
        }
        .metric-value {
            font-family: 'Syne', sans-serif;
            font-size: 2rem;
            font-weight: 800;
            color: #f0f0f0;
            line-height: 1;
        }
        .metric-delta {
            font-size: 0.8rem;
            color: #6ee7b7;
            margin-top: 0.3rem;
        }
        .section-title {
            font-family: 'Syne', sans-serif;
            font-size: 1.1rem;
            font-weight: 700;
            color: #f0f0f0;
            margin-bottom: 0.5rem;
            letter-spacing: 0.02em;
        }
        .dashboard-header {
            font-family: 'Syne', sans-serif;
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(90deg, #f0f0f0, #a0a0a0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
        }
        .dashboard-sub {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 2rem;
        }
        div[data-testid="stSelectbox"] label,
        div[data-testid="stMultiSelect"] label {
            color: #aaa;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .stMultiSelect span { background-color: #2a2a2a !important; }
        hr { border-color: #2a2a2a; }
    </style>
""", unsafe_allow_html=True)

CHART_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', color='#aaa', size=12),
    margin=dict(l=10, r=10, t=40, b=10),
    colorway=['#6ee7b7', '#60a5fa', '#f472b6', '#fb923c', '#a78bfa', '#facc15'],
    xaxis=dict(showgrid=False, zeroline=False, color='#555'),
    yaxis=dict(showgrid=True, gridcolor='#1f1f1f', zeroline=False, color='#555'),
)

@st.cache_data
def load_data():
    df = pd.read_csv('customer_behaviour_cleaned.csv')
    return df

df = load_data()

# ── Sidebar Filters ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;color:#f0f0f0;margin-bottom:1.5rem'>Filters</div>", unsafe_allow_html=True)

    seasons = st.multiselect("Season", options=sorted(df['season'].unique()), default=sorted(df['season'].unique()))
    genders = st.multiselect("Gender", options=sorted(df['gender'].unique()), default=sorted(df['gender'].unique()))
    categories = st.multiselect("Category", options=sorted(df['category'].unique()), default=sorted(df['category'].unique()))
    subscriptions = st.multiselect("Subscription", options=sorted(df['subscription_status'].unique()), default=sorted(df['subscription_status'].unique()))

    st.markdown("---")
    age_min, age_max = int(df['age'].min()), int(df['age'].max())
    age_range = st.slider("Age Range", age_min, age_max, (age_min, age_max))

filtered = df[
    df['season'].isin(seasons) &
    df['gender'].isin(genders) &
    df['category'].isin(categories) &
    df['subscription_status'].isin(subscriptions) &
    df['age'].between(age_range[0], age_range[1])
]

# ── Header ───────────────────────────────────────────────────────
st.markdown("<div class='dashboard-header'>Customer Shopping Behaviour</div>", unsafe_allow_html=True)
st.markdown("<div class='dashboard-sub'>Interactive analytics dashboard · 3,900 customers · 18 features</div>", unsafe_allow_html=True)

# ── KPI Cards ────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-label'>Total Revenue</div>
        <div class='metric-value'>${filtered['purchase_amount'].sum():,.0f}</div>
        <div class='metric-delta'>↑ across {len(filtered):,} transactions</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-label'>Avg Purchase</div>
        <div class='metric-value'>${filtered['purchase_amount'].mean():.2f}</div>
        <div class='metric-delta'>per transaction</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-label'>Avg Rating</div>
        <div class='metric-value'>{filtered['review_rating'].mean():.2f}</div>
        <div class='metric-delta'>out of 5.0</div>
    </div>""", unsafe_allow_html=True)
with k4:
    sub_pct = (filtered['subscription_status'] == 'Yes').mean() * 100
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-label'>Subscribers</div>
        <div class='metric-value'>{sub_pct:.1f}%</div>
        <div class='metric-delta'>of filtered customers</div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── Row 1: Revenue by Category | Top Items ───────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown("<div class='section-title'>Revenue by Category</div>", unsafe_allow_html=True)
    cat_rev = filtered.groupby('category')['purchase_amount'].sum().reset_index().sort_values('purchase_amount', ascending=True)
    fig = px.bar(cat_rev, x='purchase_amount', y='category', orientation='h',
                 labels={'purchase_amount': 'Total Revenue ($)', 'category': ''},
                 color='purchase_amount', color_continuous_scale=['#1f2937', '#6ee7b7'])
    fig.update_layout(**CHART_THEME, showlegend=False, coloraxis_showscale=False, height=320)
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("<div class='section-title'>Top 10 Items Purchased</div>", unsafe_allow_html=True)
    top_items = filtered['item_purchased'].value_counts().head(10).reset_index()
    top_items.columns = ['item', 'count']
    top_items = top_items.sort_values('count', ascending=True)
    fig = px.bar(top_items, x='count', y='item', orientation='h',
                 labels={'count': 'Units Sold', 'item': ''},
                 color='count', color_continuous_scale=['#1f2937', '#60a5fa'])
    fig.update_layout(**CHART_THEME, showlegend=False, coloraxis_showscale=False, height=320)
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)

# ── Row 2: Seasonal Revenue | Payment Methods ────────────────────
c3, c4 = st.columns(2)

with c3:
    st.markdown("<div class='section-title'>Revenue by Season</div>", unsafe_allow_html=True)
    season_rev = filtered.groupby('season')['purchase_amount'].sum().reset_index()
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    season_rev['season'] = pd.Categorical(season_rev['season'], categories=season_order, ordered=True)
    season_rev = season_rev.sort_values('season')
    fig = px.bar(season_rev, x='season', y='purchase_amount',
                 labels={'purchase_amount': 'Total Revenue ($)', 'season': ''},
                 color='season', color_discrete_sequence=['#6ee7b7', '#fb923c', '#f472b6', '#60a5fa'])
    fig.update_layout(**CHART_THEME, showlegend=False, height=320)
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.markdown("<div class='section-title'>Payment Method Breakdown</div>", unsafe_allow_html=True)
    pay = filtered['payment_method'].value_counts().reset_index()
    pay.columns = ['method', 'count']
    fig = px.pie(pay, names='method', values='count', hole=0.55,
                 color_discrete_sequence=['#6ee7b7', '#60a5fa', '#f472b6', '#fb923c', '#a78bfa', '#facc15'])
    fig.update_layout(**CHART_THEME, height=320,
                      legend=dict(orientation='v', x=1, y=0.5, font=dict(color='#aaa')))
    fig.update_traces(textfont_color='#f0f0f0', textfont_size=12)
    st.plotly_chart(fig, use_container_width=True)

# ── Row 3: Age Group Analysis | Subscription Comparison ──────────
c5, c6 = st.columns(2)

with c5:
    st.markdown("<div class='section-title'>Purchase Amount by Age Group & Gender</div>", unsafe_allow_html=True)
    age_gen = filtered.groupby(['age_group', 'gender'])['purchase_amount'].mean().reset_index()
    age_order = ['Young adult', 'Adult', 'Mid-aged', 'Senior']
    age_gen['age_group'] = pd.Categorical(age_gen['age_group'], categories=age_order, ordered=True)
    age_gen = age_gen.sort_values('age_group')
    fig = px.bar(age_gen, x='age_group', y='purchase_amount', color='gender', barmode='group',
                 labels={'purchase_amount': 'Avg Purchase ($)', 'age_group': '', 'gender': ''},
                 color_discrete_map={'Male': '#60a5fa', 'Female': '#f472b6'})
    fig.update_layout(**CHART_THEME, height=320,
                      legend=dict(orientation='h', y=1.1, x=0, font=dict(color='#aaa')))
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)

with c6:
    st.markdown("<div class='section-title'>Subscribers vs Non-Subscribers</div>", unsafe_allow_html=True)
    sub = filtered.groupby('subscription_status').agg(
        avg_purchase=('purchase_amount', 'mean'),
        avg_rating=('review_rating', 'mean'),
        avg_prev_purchases=('previous_purchases', 'mean')
    ).reset_index()
    fig = go.Figure()
    metrics = ['avg_purchase', 'avg_rating', 'avg_prev_purchases']
    labels = ['Avg Purchase ($)', 'Avg Rating', 'Avg Prev Purchases']
    colors = {'Yes': '#6ee7b7', 'No': '#60a5fa'}
    for _, row in sub.iterrows():
        vals = [row[m] for m in metrics]
        fig.add_trace(go.Bar(
            name=f"{'Subscribed' if row['subscription_status'] == 'Yes' else 'Not Subscribed'}",
            x=labels, y=vals,
            marker_color=colors[row['subscription_status']],
            marker_line_width=0
        ))
    fig.update_layout(**CHART_THEME, barmode='group', height=320,
                      legend=dict(orientation='h', y=1.1, x=0, font=dict(color='#aaa')))
    st.plotly_chart(fig, use_container_width=True)

# ── Row 4: Purchase Distribution | Top Locations ─────────────────
c7, c8 = st.columns(2)

with c7:
    st.markdown("<div class='section-title'>Purchase Amount Distribution</div>", unsafe_allow_html=True)
    fig = px.box(filtered, x='category', y='purchase_amount', color='category',
                 labels={'purchase_amount': 'Purchase Amount ($)', 'category': ''},
                 color_discrete_sequence=['#6ee7b7', '#60a5fa', '#f472b6', '#fb923c'])
    fig.update_layout(**CHART_THEME, height=320, showlegend=False)
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)

with c8:
    st.markdown("<div class='section-title'>Top 10 Locations by Revenue</div>", unsafe_allow_html=True)
    loc_rev = filtered.groupby('location')['purchase_amount'].sum().nlargest(10).reset_index().sort_values('purchase_amount', ascending=True)
    fig = px.bar(loc_rev, x='purchase_amount', y='location', orientation='h',
                 labels={'purchase_amount': 'Total Revenue ($)', 'location': ''},
                 color='purchase_amount', color_continuous_scale=['#1f2937', '#facc15'])
    fig.update_layout(**CHART_THEME, showlegend=False, coloraxis_showscale=False, height=320)
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)

# ── Row 5: Purchase Frequency ─────────────────────────────────────
st.markdown("<div class='section-title'>Purchase Frequency Distribution</div>", unsafe_allow_html=True)
freq_order = ['Weekly', 'Bi-Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Every 3 Months', 'Annually']
freq = filtered['frequency_of_purchases'].value_counts().reindex(freq_order).reset_index()
freq.columns = ['frequency', 'count']
fig = px.bar(freq, x='frequency', y='count',
             labels={'count': 'Number of Customers', 'frequency': ''},
             color='count', color_continuous_scale=['#1f2937', '#fb923c'])
fig.update_layout(**CHART_THEME, showlegend=False, coloraxis_showscale=False, height=300)
fig.update_traces(marker_line_width=0)
st.plotly_chart(fig, use_container_width=True)

st.markdown("<div style='color:#444;font-size:0.8rem;text-align:center;margin-top:2rem'>Customer Shopping Behaviour Dashboard · Built with Streamlit & Plotly</div>", unsafe_allow_html=True)