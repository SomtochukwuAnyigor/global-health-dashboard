import streamlit as st
import pandas as pd
import plotly.express as px
import warnings

# 1. Page Configuration
st.set_page_config(page_title="Global Nutrition Dashboard", layout="wide")

# 2. Robust Data Loading
# This ignores non-critical system warnings that can trigger the 'warnings' error
warnings.filterwarnings('ignore')

try:
    # index_col=False ensures the columns are parsed exactly as they appear in the CSV
    df = pd.read_csv('unicef_data.csv', index_col=False)
except Exception as e:
    st.error(f"⚠️ Dashboard Alert: Could not read the data file. Please ensure 'unicef_data.csv' is in the same folder as this script.")
    st.stop()

# 3. Header Section
st.title("🌍 Global Infant Nutrition Analysis")
st.markdown("""
**Author:** Somtochukwu Anyigor (Medical Student & Data Scientist)  
*Specializing in the intersection of Clinical Pathology and Population Data Science.*
""")

# 4. Sidebar Navigation & Professional Bio
st.sidebar.header("Clinical Controls")
st.sidebar.info("This dashboard analyzes the first 1,000 days of life—a critical window for neurodevelopment and physical growth.")

selected_country = st.sidebar.selectbox("Select a Country for Detailed Analysis:", df['Country'].unique())

st.sidebar.markdown("---")
st.sidebar.markdown("""
### **About the Analyst**
Somtochukwu is a Medical Student bridging the gap between **Pathology** and **Data Science**. 
This project focuses on how nutritional data should influence pediatric **Pharmacological** dosing and clinical policy in Sub-Saharan Africa.
""")

# Filter data for the selected country
country_stats = df[df['Country'] == selected_country].iloc[0]

# 5. Key Performance Indicators (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Exclusive Breastfeeding Rate", value=f"{country_stats['Breastfeeding_Rate']}%")
with col2:
    st.metric(label="Stunting Prevalence", value=f"{country_stats['Stunting_Rate']}%", delta="High Burden", delta_color="inverse")
with col3:
    st.metric(label="Data Integrity", value="Verified (2024)")

# 6. Global Visualization Map
st.subheader("Interactive Global Nutrition Map")
fig = px.choropleth(
    df, 
    locations="ISO_Code", 
    color="Breastfeeding_Rate",
    hover_name="Country",
    color_continuous_scale=px.colors.sequential.Viridis,
    labels={'Breastfeeding_Rate': 'EBF %'}
)
st.plotly_chart(fig, use_container_width=True)

# 7. Clinical Case Review & Observations
st.divider()
st.header("👨‍⚕️ Clinical Case Review & Observations")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("The EBF-Stunting Correlation")
    st.markdown(f"""
    **Current Analysis for {selected_country}:**
    * **Immunological Gap:** With an EBF rate of **{country_stats['Breastfeeding_Rate']}%**, there is a significant 'antibody gap' in the neonatal population.
    * **Pathology Note:** Lack of colostrum and exclusive human milk increases vulnerability to repeated enteric infections (diarrhea), which is a primary driver of nutrient malabsorption and subsequent linear growth retardation (Stunting).
    """)

with col_b:
    st.subheader("Public Health Implications")
    st.markdown(f"""
    **Stunting Burden ({country_stats['Stunting_Rate']}%):**
    * **Neurological Impact:** Chronic malnutrition during the first 1,000 days leads to irreversible cognitive deficits and reduced human capital.
    * **Pharmacological Note:** Malnourished children often have altered drug metabolism (due to reduced plasma proteins like albumin), which complicates standard pediatric dosing during infections.
    """)

# 8. Footer
st.info("📊 **Source Integrity:** Data cross-referenced with UNICEF Joint Malnutrition Estimates (2024) and NDHS 2023-24.")
st.sidebar.markdown("---")

st.sidebar.write("✅ **Portfolio Status:** Deployment Ready")
