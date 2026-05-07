import streamlit as st
from groq import Groq
import feedparser
import requests
from PIL import Image

# 1. PAGE SETUP & LOGO
st.set_page_config(page_title="CAPO Master Sentinel", layout="wide")

# This section handles your logo. Ensure your file is named "logo.png" on GitHub.
try:
    logo = Image.open("logo.png") 
    col_l, col_r = st.columns([1, 6])
    with col_l:
        st.image(logo, width=120)
    with col_r:
        st.title("CAPO Consulting: Master Sentinel")
        st.markdown("*Strategic Intelligence: Nutrition | Social Protection | Emergency*")
except FileNotFoundError:
    st.title("📡 CAPO Consulting: Master Sentinel")
    st.info("💡 To show your logo, upload a file named 'logo.png' to your GitHub repository.")

# 2. 2026 NATIONAL BENCHMARKS (DATA VISUALIZATION)
with st.expander("📊 2026 National Nutrition Benchmarks", expanded=False):
    c1, c2, c3 = st.columns(3)
    c1.metric("Stunting (National)", "37.6%", "Trend: Reversing")
    c2.metric("Wasting (U5)", "2.0%", "Status: Target Met")
    c3.metric("SCTP Reach", "303k HH", "Mtukula Pakhomo")
    st.caption("Baseline: May 2026 NNIS/SUN Mirror Data")

# 3. SECURE CONNECTION TO AI
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 4. AUTOMATED NEWS SCANNER ENGINE
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
            if resp.status_code == 200:
                feed = feedparser.parse(resp.content)
                for entry in feed.entries[:3]:
                    all_news.append({
                        "title": entry.title, 
                        "summary": entry.get('summary', 'New report available.'), 
                        "source": name
                    })
        except:
            continue
    return all_news

# 5. SIDEBAR COMMAND CENTER
with st.sidebar:
    st.header("Intelligence Controls")
    if st.button("🚀 SCAN LIVE TECH FEEDS", use_container_width=True):
        st.session_state['news_feeds'] = fetch_automated_intel()
    
    st.divider()
    st.subheader("🤖 AI Research / Manual Input")
    st.caption("No news? Type a topic to generate a strategy.")
    m_topic = st.text_input("Subject (e.g. Neno Floods)")
    m_context = st.text_area("Context (e.g. News headline)")
    if st.button("Generate Strategy from Input"):
        st.session_state['active_item'] = {"title": m_topic, "summary": m_context}

# 6. DASHBOARD LAYOUT
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🗞️ Captured Intel")
    if 'news_feeds' in st.session_state and st.session_state['news_feeds']:
        for i, item in enumerate(st.session_state['news_feeds']):
            with st.container(border=True):
                st.caption(f"Source: {item['source']}")
                st.subheader(item['title'])
                if st.button("Analyze Impact", key=f"feed_{i}"):
                    st.session_state['active_item'] = item
    else:
        st.info("System Ready. Click 'Scan' or use 'AI Research' in the sidebar.")

with col2:
    st.header("🧠 CAPO Strategic Narrative")
    if 'active_item' in st.session_state:
        target = st.session_state['active_item']
        
        # Linking logic for the AI
        master_prompt = f"""
        Role: Lead Consultant, CAPO. 
        Context: Malawi 2026 (Stunting: 37.6%, Wasting: 2.0%, SCTP: 303k HH).
        Current Topic: {target['title']}
        Summary/Text: {target['summary']}
        
        TASKS:
        1. DATA LINK: How does this specific news/topic impact the 37.6% stunting or 2% wasting benchmarks?
        2. CHANGE MANAGEMENT: Analyze this from the 'Ownership vs Compliance' perspective.
        3. SOCIAL PROTECTION: How should the Social Cash Transfer Program (SCTP) be leveraged here?
        4. LINKEDIN POST: Write a high-impact post that positions me as a data-driven expert.
        """
        
        with st.spinner("Synthesizing multi-sectoral narrative..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": master_prompt}],
            )
            st.success("Master Analysis Generated!")
            st.markdown(completion.choices[0].message.content)
