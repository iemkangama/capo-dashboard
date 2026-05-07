import streamlit as st
from groq import Groq
import feedparser
import requests

# 1. Branding & Master Setup
st.set_page_config(page_title="CAPO Master Sentinel", layout="wide")
st.title("📡 CAPO Consulting: Master Sentinel")
st.markdown("*Real-time Intelligence for Malawi's Nutrition, Social Protection & Emergencies*")

# 2. Connection
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. The "Fail-Proof" Scraper
def get_intel():
    # We use multiple sources to ensure at least one works
    feeds = {
        "ReliefWeb Malawi": "https://reliefweb.int/country/mwi/rss.xml",
        "IFPRI Malawi": "https://massp.ifpri.info/feed/",
        "SUN Movement": "https://scalingupnutrition.org/news/feed"
    }
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    intel_bank = []
    
    for name, url in feeds.items():
        try:
            # We use a 5-second timeout so the app doesn't hang
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                feed = feedparser.parse(resp.content)
                for entry in feed.entries[:3]:
                    intel_bank.append({
                        "title": entry.title,
                        "summary": entry.get('summary', 'New report available.'),
                        "source": name
                    })
        except:
            continue
    return intel_bank

# 4. Sidebar: The Command Center
with st.sidebar:
    st.header("Sentinel Controls")
    if st.button("🚀 SCAN FOR LIVE NEWS", use_container_width=True):
        st.session_state['data'] = get_intel()
        if not st.session_state['data']:
            st.warning("Live feeds are currently restricted. Use 'AI Research Mode' below.")

    st.divider()
    st.subheader("🤖 AI Research Mode")
    st.info("No live news? Tell the AI what topic to research for your LinkedIn post.")
    research_topic = st.text_input("e.g., 'SCTP in Phalombe' or 'Stunting in 2026'")
    if st.button("Generate Strategy from AI Knowledge"):
        st.session_state['active_item'] = {"title": "AI Strategic Analysis", "summary": research_topic}

# 5. Dashboard Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🗞️ Captured Intel")
    if 'data' in st.session_state and st.session_state['data']:
        for i, item in enumerate(st.session_state['data']):
            with st.container(border=True):
                st.caption(f"Source: {item['source']}")
                st.subheader(item['title'])
                if st.button("Analyze for LinkedIn", key=f"btn_{i}"):
                    st.session_state['active_item'] = item
    else:
        st.info("System Ready. Click 'Scan' or use 'AI Research Mode' in the sidebar.")

with col2:
    st.header("🧠 Consultant Analysis")
    if 'active_item' in st.session_state:
        target = st.session_state['active_item']
        
        prompt = f"""
        Role: Senior Consultant for CAPO.
        Subject: {target['title']}
        Summary/Context: {target['summary']}
        
        Task:
        1. Link this to Nutrition Outcomes (Stunting/MDD), Social Protection (SCTP), and Emergency Response.
        2. Analyze the 'Ownership vs Compliance' risk.
        3. Draft a LinkedIn post that emphasizes 'Change Management' and 'Sustainability'.
        """
        
        with st.spinner("AI Brain synthesizing..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
            )
            st.success("Master Analysis Generated!")
            st.markdown(completion.choices[0].message.content)
