import streamlit as st
from groq import Groq
import feedparser
import requests

# 1. Branding & Master Setup
st.set_page_config(page_title="CAPO Master Sentinel", layout="wide")
st.title("📡 CAPO Consulting: Master Sentinel")
st.markdown("*Real-time Intelligence for Malawi's Nutrition & Food Systems*")

# 2. Secure Connection
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. The "Reliable" Scraper Engine
def get_intel():
    # Targeted feeds that are currently active and stable in 2026
    feeds = {
        "ReliefWeb Malawi": "https://reliefweb.int/country/mwi/rss.xml",
        "IFPRI Malawi": "https://www.ifpri.org/program/malawi-strategy-support-program/feed",
        "SUN Movement": "https://scalingupnutrition.org/news/feed"
    }
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    intel_bank = []
    
    status_placeholder = st.empty() # For live updates
    
    for name, url in feeds.items():
        status_placeholder.text(f"📡 Accessing {name}...")
        try:
            # We use 'requests' to get the content first, which is more reliable
            resp = requests.get(url, headers=headers, timeout=10)
            feed = feedparser.parse(resp.content)
            
            for entry in feed.entries[:5]: # Take top 5
                intel_bank.append({
                    "title": entry.title,
                    "summary": entry.get('summary', 'New report available.'),
                    "source": name,
                    "link": entry.link
                })
        except Exception as e:
            st.sidebar.warning(f"Note: {name} is temporarily unreachable.")
    
    status_placeholder.empty()
    return intel_bank

# 4. Sidebar: The Command Center
with st.sidebar:
    st.header("Sentinel Controls")
    if st.button("🚀 RUN FULL SYSTEM SCAN", use_container_width=True):
        st.session_state['data'] = get_intel()
    
    st.divider()
    st.subheader("Manual Backup")
    m_title = st.text_input("Report Title")
    m_text = st.text_area("Summary/Content")
    if st.button("Analyze Manual Entry"):
        st.session_state['active_item'] = {"title": m_title, "summary": m_text}

# 5. The Dashboard Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🗞️ Captured Reports")
    if 'data' in st.session_state and st.session_state['data']:
        for i, item in enumerate(st.session_state['data']):
            with st.container(border=True):
                st.caption(f"Source: {item['source']}")
                st.subheader(item['title'])
                if st.button("Analyze for LinkedIn", key=f"btn_{i}"):
                    st.session_state['active_item'] = item
    else:
        st.info("System Ready. Click the 'Scan' button in the sidebar to hunt for data.")

with col2:
    st.header("🧠 Consultant Analysis")
    if 'active_item' in st.session_state:
        target = st.session_state['active_item']
        
        prompt = f"""
        Role: Senior Consultant for CAPO.
        Subject: {target['title']}
        Summary: {target['summary']}
        
        Task:
        1. Discuss the link between Nutrition (Stunting/MDD), Social Protection (SCTP), and Emergency Response.
        2. Analyze the 'Ownership vs Compliance' angle.
        3. Draft a high-impact LinkedIn post that positions me as a Project Management expert. 
           Include a visual analogy like 'The House of Resilience.'
        """
        
        with st.spinner("AI Brain synthesizing..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
            )
            st.success("Master Analysis Generated!")
            st.markdown(completion.choices[0].message.content)
