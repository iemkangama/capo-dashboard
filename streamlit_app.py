import streamlit as st
from groq import Groq
import feedparser

# 1. Branding
st.set_page_config(page_title="CAPO Master Sentinel", layout="wide")
st.title("📡 CAPO Consulting: Master Sentinel")

# 2. Connection
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Master Keywords (Broadened slightly to ensure results)
TECHNICAL_KEYWORDS = [
    "nutrition", "stunting", "wasting", "food", "maize", "sctp", 
    "cash", "emergency", "malawi", "health", "unicef", "wfp", "harvest"
]

# 4. Master Scraper with Status Updates
def fetch_master_intel():
    feeds = {
        "ReliefWeb (UN/NGOs)": "https://reliefweb.int/country/mwi/rss.xml",
        "SUN Movement": "https://scalingupnutrition.org/news/feed",
        "FEWS NET (Food Security)": "https://fews.net/southern-africa/malawi/rss.xml"
    }
    all_data = []
    
    for name, url in feeds.items():
        st.write(f"🔍 Sentinel is hunting on: {name}...") # Status Nudge
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                content = (entry.title + entry.get('summary', '')).lower()
                
                # Check for keywords
                is_tech = any(key in content for key in TECHNICAL_KEYWORDS)
                
                all_data.append({
                    "title": entry.title,
                    "summary": entry.get('summary', 'Click link for full report.'),
                    "link": entry.link,
                    "is_technical": is_tech
                })
        except Exception as e:
            st.error(f"Could not reach {name}")
    return all_data

# 5. Sidebar
if st.sidebar.button("🔍 Run Full System Scan"):
    st.session_state['master_intel'] = fetch_master_intel()

# 6. Dashboard Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🗞️ Captured Intel")
    if 'master_intel' in st.session_state and st.session_state['master_intel']:
        # NEW: Option to show all news if technical filter is too strict
        show_all = st.checkbox("Show all Malawi news (even non-technical)")
        
        for i, item in enumerate(st.session_state['master_intel']):
            if item['is_technical'] or show_all:
                with st.container(border=True):
                    st.subheader(item['title'])
                    if st.button("Analyze for LinkedIn", key=f"btn_{i}"):
                        st.session_state['active_item'] = item
    else:
        st.info("System idle. Click 'Run Full System Scan' to begin.")

with col2:
    st.header("🧠 Consultant Analysis")
    if 'active_item' in st.session_state:
        target = st.session_state['active_item']
        prompt = f"Analyze as CAPO Consulting Lead: {target['title']}. Link to Nutrition, Social Protection, and Emergency Response. Draft a LinkedIn post."
        
        with st.spinner("Synthesizing..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
            )
            st.markdown(completion.choices[0].message.content)
