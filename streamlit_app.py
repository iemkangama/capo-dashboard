import streamlit as st
from groq import Groq
import feedparser
import requests

# 1. Page Config & National Benchmarks
st.set_page_config(page_title="CAPO Master Sentinel", layout="wide")
st.title("📡 CAPO Consulting: Strategic Sentinel")

with st.expander("📊 2026 National Nutrition Benchmarks", expanded=False):
    c1, c2, c3 = st.columns(3)
    c1.metric("Stunting (National)", "37.6%", "Trend: Reversing")
    c2.metric("Wasting (U5)", "2.0%", "Status: Target Met")
    c3.metric("SCTP Reach", "303k HH", "Mtukula Pakhomo")
    st.caption("Data source: NNIS/SUN Mirror (May 2026)")

# 2. Connection
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Enhanced Automated Scraper
def fetch_automated_intel():
    feeds = {
        "ReliefWeb (UNICEF/WFP)": "https://reliefweb.int/country/mwi/rss.xml",
        "SUN Movement": "https://scalingupnutrition.org/news/feed",
        "IFPRI Malawi": "https://massp.ifpri.info/feed/"
    }
    headers = {'User-Agent': 'Mozilla/5.0'}
    all_news = []
    
    for name, url in feeds.items():
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            feed = feedparser.parse(resp.content)
            for entry in feed.entries[:3]:
                all_news.append({"title": entry.title, "summary": entry.get('summary', ''), "source": name})
        except: continue
    return all_news

# 4. Sidebar: Automated & Manual Controls
with st.sidebar:
    st.header("Intelligence Controls")
    if st.button("🔍 Scan Live Tech Feeds", use_container_width=True):
        st.session_state['news_feeds'] = fetch_automated_intel()
    
    st.divider()
    st.subheader("Manual Override")
    m_topic = st.text_input("Enter Subject")
    m_context = st.text_area("Paste Report/Headline")
    if st.button("Analyze Manual Input"):
        st.session_state['active_item'] = {"title": m_topic, "summary": m_context}

# 5. Dashboard Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🗞️ Automated Intelligence")
    if 'news_feeds' in st.session_state and st.session_state['news_feeds']:
        for i, item in enumerate(st.session_state['news_feeds']):
            with st.container(border=True):
                st.caption(item['source'])
                st.subheader(item['title'])
                if st.button("Analyze Impact", key=f"feed_{i}"):
                    st.session_state['active_item'] = item
    else:
        st.info("Click 'Scan Live Tech Feeds' in the sidebar or use Manual Override.")

with col2:
    st.header("🧠 CAPO Strategic Narrative")
    if 'active_item' in st.session_state:
        target = st.session_state['active_item']
        
        # Benchmarks passed into the prompt
        prompt = f"""
        Role: Lead Consultant, CAPO. 
        Context: Malawi 2026 (Stunting: 37.6%, Wasting: 2.0%, SCTP: 303k HH).
        Topic: {target['title']}
        Summary: {target['summary']}
        
        1. NARRATIVE: How does this impact our national targets?
        2. PM/CHANGE: Ownership vs Compliance analysis.
        3. SOCIAL PROTECTION: Role of SCTP/Safety Nets here.
        4. LINKEDIN POST: Write a data-backed post for CAPO.
        """
        
        with st.spinner("AI Brain synthesizing..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
            )
            st.success("Analysis Ready!")
            st.markdown(completion.choices[0].message.content)
