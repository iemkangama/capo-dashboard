import streamlit as st
from groq import Groq
import feedparser
import requests
from PIL import Image

# 1. PAGE SETUP
st.set_page_config(page_title="CAPO Master Sentinel", layout="wide")

# 2. BRANDING (MALAWIAN CONTEXT)
try:
    logo = Image.open("Capo_Consulting_Logo.png") 
    col_l, col_r = st.columns([1, 6])
    with col_l: st.image(logo, width=120)
    with col_r:
        st.title("CAPO Consulting: Strategic Sentinel")
        st.markdown("### *Malawi Priority & SADC Regional Intelligence Hub*")
except:
    st.title("📡 CAPO Consulting: Strategic Sentinel")

# 3. NATIONAL & REGIONAL DATA BANK
with st.expander("📊 National & Regional Benchmarks (2026)", expanded=True):
    m1, m2, m3 = st.columns(3)
    m1.metric("Malawi Stunting", "37.6%", "Alert: Reversing")
    m2.metric("SADC Avg Stunting", "30.3%", "Target: <20%")
    m3.metric("Wasting (MW)", "2.0%", "Status: Target Met")

# 4. INTELLIGENT SCANNER (MALAWIAN PRIORITY)
def fetch_intel():
    # Priority 1: Malawi Specific
    # Priority 2: Regional/SADC
    feeds = [
        {"name": "ReliefWeb Malawi", "url": "https://reliefweb.int/country/mwi/rss.xml", "priority": 1},
        {"name": "IFPRI Malawi (MaSSP)", "url": "https://massp.ifpri.info/feed/", "priority": 1},
        {"name": "UNICEF Malawi", "url": "https://reliefweb.int/organization/unicef/rss.xml?source=146", "priority": 1},
        {"name": "SADC Regional News", "url": "https://reliefweb.int/countries/southern-africa/rss.xml", "priority": 2}
    ]
    
    # We use a 'Real Browser' header to stop servers from blocking us (Fixes the blank results)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) CAPO-Sentinel/2.0'}
    intel_bank = []
    
    for feed in feeds:
        try:
            resp = requests.get(feed['url'], headers=headers, timeout=10)
            parsed = feedparser.parse(resp.content)
            for entry in parsed.entries[:4]:
                intel_bank.append({
                    "title": entry.title,
                    "summary": entry.get('summary', 'Detailed report inside.'),
                    "source": feed['name'],
                    "priority": feed['priority']
                })
        except: continue
    
    # SORTING: Ensure Priority 1 (Malawi) always appears at the top
    return sorted(intel_bank, key=lambda x: x['priority'])

# 5. SIDEBAR CONTROLS
with st.sidebar:
    st.header("Intelligence Controls")
    if st.button("🔍 RUN MALAWI-FIRST SCAN", use_container_width=True):
        st.session_state['data'] = fetch_intel()
    
    st.divider()
    st.subheader("Manual Input (Alternative)")
    m_topic = st.text_input("Enter Topic")
    m_context = st.text_area("Paste Content")
    if st.button("Analyze Manual Input"):
        st.session_state['active'] = {"title": m_topic, "summary": m_context}

# 6. DASHBOARD DISPLAY
col_left, col_right = st.columns([1, 1])

with col_left:
    st.header("🗞️ Scanned Reports")
    if 'data' in st.session_state and st.session_state['data']:
        for i, item in enumerate(st.session_state['data']):
            with st.container(border=True):
                # Highlight Malawi results with a badge
                if item['priority'] == 1: st.write("🇲🇼 **MALAWI PRIORITY**")
                else: st.write("🌍 REGIONAL")
                st.subheader(item['title'])
                st.caption(f"Source: {item['source']}")
                if st.button("Link to Strategy", key=f"f_{i}"):
                    st.session_state['active'] = item
    else:
        st.info("The scanner is ready. Click the button in the sidebar to fetch live 2026 data.")

with col_right:
    st.header("🧠 CAPO Analysis")
    if 'active' in st.session_state:
        target = st.session_state['active']
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        prompt = f"""
        Analyze this report from the perspective of CAPO Consulting.
        Topic: {target['title']}
        Summary: {target['summary']}
        Malawi Baseline: Stunting 37.6%, Wasting 2.0%. 
        SADC Context: Regional stunting at 30.3%.
        
        Provide:
        1. Strategic Impact on Malawi's Nutrition Targets.
        2. Ownership vs Compliance analysis.
        3. A LinkedIn post comparing this specific district/country event to the wider SADC trend.
        """
        
        with st.spinner("Processing..."):
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
            st.markdown(res.choices[0].message.content)
