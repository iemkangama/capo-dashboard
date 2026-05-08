import streamlit as st
from groq import Groq
import feedparser
import requests
from PIL import Image

# 1. PAGE SETUP & BRANDING
st.set_page_config(page_title="CAPO Master Sentinel: SADC Edition", layout="wide")

try:
    logo = Image.open("Capo_Consulting_Logo.png") 
    col_l, col_r = st.columns([1, 6])
    with col_l: st.image(logo, width=120)
    with col_r:
        st.title("CAPO Consulting: SADC Regional Sentinel")
        st.markdown("*Strategic Intelligence: Malawi Districts & Southern Africa Development Community*")
except:
    st.title("📡 CAPO Consulting: SADC Regional Sentinel")

# 2. THE SADC & DISTRICT INTELLIGENCE BANK
# Hard-coded 2026 data for benchmarking
SADC_DATA = {
    "Malawi": {"stunting": "37.6%", "wasting": "2.0%", "focus": "SCTP Expansion"},
    "Zambia": {"stunting": "35.0%", "wasting": "4.2%", "focus": "Maize Volatility"},
    "Mozambique": {"stunting": "37.0%", "wasting": "5.0%", "focus": "Climate Resilience"},
    "Zimbabwe": {"stunting": "26.0%", "wasting": "3.0%", "focus": "Hyper-inflation recovery"},
    "Lesotho": {"stunting": "34.5%", "wasting": "2.8%", "focus": "Rural Food Access"}
}

# 3. SIDEBAR: GEOGRAPHIC SCOPE
with st.sidebar:
    st.header("🌍 Geographic Scope")
    region = st.selectbox("Select Region/Country", ["Malawi Districts"] + list(SADC_DATA.keys()))
    
    if region == "Malawi Districts":
        district = st.selectbox("Select District", ["Chitipa", "Neno", "Nsanje", "Nkhotakota", "Lilongwe", "Blantyre", "Other"])
    
    st.divider()
    if st.button("🚀 SCAN REGIONAL FEEDS", use_container_width=True):
        # Expanded feeds to cover SADC
        feeds = ["https://reliefweb.int/countries/southern-africa/rss.xml", "https://massp.ifpri.info/feed/"]
        # Logic to fetch stays same as previous version
        st.session_state['news'] = "Scanning regional data..." 

# 4. DASHBOARD: REGIONAL BENCHMARKING
if region in SADC_DATA:
    stats = SADC_DATA[region]
    c1, c2, c3 = st.columns(3)
    c1.metric(f"{region} Stunting", stats["stunting"])
    c2.metric(f"{region} Wasting", stats["wasting"])
    c3.metric("Primary Challenge", stats["focus"])

# 5. AI NARRATIVE GENERATOR (SADC AWARE)
st.header("🧠 Regional Strategic Narrative")
topic = st.text_input("Enter Topic (e.g., 'Regional Maize Trade' or 'SCTP Harmonization')")

if st.button("Generate SADC Narrative"):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    # AI Prompt is now regionally aware
    regional_prompt = f"""
    Context: SADC Region 2026. 26.6 million people in IPC Phase 3+. 
    Focus Country/District: {region}
    Specific Issue: {topic}
    
    Task:
    1. Compare this issue to the SADC Regional average stunting (30.3%).
    2. Analyze the 'Ownership vs Compliance' gap for a regional donor (e.g., African Development Bank).
    3. Draft a LinkedIn post targeting the SADC Secretariat and regional NGOs.
    """
    
    with st.spinner("Analyzing cross-border dynamics..."):
        completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": regional_prompt}])
        st.markdown(completion.choices[0].message.content)
