import streamlit as st
from groq import Groq
import feedparser
import requests
from PIL import Image

# 1. PAGE SETUP & LOGO
st.set_page_config(page_title="CAPO Master Sentinel", layout="wide")

try:
    logo = Image.open("Capo_Consulting_Logo.png") 
    col_l, col_r = st.columns([1, 6])
    with col_l: st.image(logo, width=120)
    with col_r:
        st.title("CAPO Consulting: Strategic Sentinel")
        st.markdown("### *Evidence & Operational Intelligence Hub*")
except:
    st.title("📡 CAPO Consulting: Strategic Sentinel")

# 2. NATIONAL & REGIONAL DATA BANK (May 2026)
with st.expander("📊 May 2026 Nutrition Benchmarks", expanded=True):
    m1, m2, m3 = st.columns(3)
    m1.metric("National Stunting", "37.6%", "Trend: 0.5pp Reversal")
    m2.metric("National Wasting", "2.0%", "Status: Target Met")
    m3.metric("SADC Regional Stunting", "30.3%", "Target: <20%")
    st.caption("Hotspots: Chitipa (50.8%), Neno (50.0%), Southern Region (38.7%)")

# 3. SCANNING LOGIC
def fetch_intel(category):
    # Category 1: Academic & Peer-Reviewed
    if category == "academic":
        feeds = [
            {"name": "Malawi Medical Journal (MMJ)", "url": "https://www.mmj.mw/feed/"},
            {"name": "IFPRI/LUANAR Research", "url": "https://massp.ifpri.info/feed/"},
            {"name": "ZEF/GIZ Policy Briefs", "url": "https://reliefweb.int/organization/giz/rss.xml"}
        ]
        keywords = ['nutrition', 'stunting', 'wasting', 'food', 'SCTP', 'diet', 'agriculture', 'determinants']
    
    # Category 2: UN, SUN, Media, and SADC Operations
    else:
        feeds = [
            {"name": "ReliefWeb Malawi (UN/NGO)", "url": "https://reliefweb.int/country/mwi/rss.xml"},
            {"name": "SUN Movement News", "url": "https://scalingupnutrition.org/news/feed"},
            {"name": "SADC Regional Updates", "url": "https://reliefweb.int/countries/southern-africa/rss.xml"},
            {"name": "FAO/WFP Bulletins", "url": "https://reliefweb.int/organization/wfp/rss.xml?country=146"}
        ]
        keywords = None # No filter for operational news

    headers = {'User-Agent': 'Mozilla/5.0'}
    results = []
    
    for feed in feeds:
        try:
            resp = requests.get(feed['url'], headers=headers, timeout=10)
            parsed = feedparser.parse(resp.content)
            for entry in parsed.entries[:5]:
                # Filter academic results for relevance
                if keywords:
                    if not any(k in entry.title.lower() or k in entry.get('summary', '').lower() for k in keywords):
                        continue
                
                results.append({
                    "title": entry.title,
                    "summary": entry.get('summary', 'Details in full report.'),
                    "source": feed['name'],
                    "link": entry.link,
                    "type": "🎓 Academic" if category == "academic" else "🗞️ Operational"
                })
        except: continue
    return results

# 4. SIDEBAR COMMANDS
with st.sidebar:
    st.header("Intelligence Scans")
    if st.button("🎓 ACADEMIC RESEARCH", use_container_width=True):
        st.session_state['active_scan'] = fetch_intel("academic")
        
    if st.button("🗞️ OTHER SCANS (UN/SUN/SADC)", use_container_width=True):
        st.session_state['active_scan'] = fetch_intel("other")
    
    st.divider()
    st.subheader("Manual Input")
    m_topic = st.text_input("Enter Topic")
    m_context = st.text_area("Paste Report Text")
    if st.button("Analyze Manual Entry"):
        st.session_state['selected'] = {"title": m_topic, "summary": m_context, "type": "Manual"}

# 5. DASHBOARD DISPLAY
c_left, c_right = st.columns([1, 1])

with c_left:
    st.header("🔍 Captured Intelligence")
    if 'active_scan' in st.session_state and st.session_state['active_scan']:
        for i, item in enumerate(st.session_state['active_scan']):
            with st.container(border=True):
                st.caption(item['type'])
                st.subheader(item['title'])
                st.write(f"Source: {item['source']}")
                if st.button("Analyze Strategically", key=f"btn_{i}"):
                    st.session_state['selected'] = item
    else:
        st.info("Select a scan type in the sidebar to begin.")

with c_right:
    st.header("🧠 CAPO Strategic Synthesis")
    if 'selected' in st.session_state:
        target = st.session_state['selected']
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        prompt = f"""
        Role: Senior Consultant, CAPO.
        Analyzing: {target['title']}
        Summary: {target['summary']}
        
        Provide:
        1. STRATEGIC LINK: How does this impact Malawi's stunting (37.6%) vs wasting (2%) gap?
        2. OWNERSHIP: What change management advice should be given to the relevant Ministry?
        3. REGIONAL: Compare this to the SADC stunting average (30.3%).
        4. LINKEDIN: Write a data-rich post.
        """
        
        with st.spinner("Synthesizing..."):
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
            st.markdown(res.choices[0].message.content)
            if 'link' in target: st.link_button("View Source", target['link'])
