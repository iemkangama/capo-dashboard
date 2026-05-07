import streamlit as st
from groq import Groq
import feedparser
import requests

# 1. Page Branding
st.set_page_config(page_title="CAPO Master Sentinel", layout="wide")
st.title("📡 CAPO Consulting: Master Sentinel")
st.caption("Tracking Nutrition, Social Protection, and Emergencies in Malawi")

# 2. Connection
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Master Scraper with "Human-Mask" Headers
def fetch_news_safely():
    feeds = {
        "ReliefWeb (UN/NGOs)": "https://reliefweb.int/country/mwi/rss.xml",
        "SUN Movement": "https://scalingupnutrition.org/news/feed"
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    results = []
    
    for name, url in feeds.items():
        try:
            # We "disguise" the request as a real browser
            response = requests.get(url, headers=headers, timeout=10)
            feed = feedparser.parse(response.content)
            for entry in feed.entries[:5]:
                results.append({
                    "title": entry.title,
                    "summary": entry.get('summary', 'Open report for details.'),
                    "source": name
                })
        except:
            continue
    return results

# 4. Sidebar Controls
with st.sidebar:
    st.header("Sentinel Controls")
    if st.button("🔍 Run Full System Scan"):
        st.session_state['master_intel'] = fetch_news_safely()
    
    st.divider()
    st.header("Manual Input")
    st.info("No news found? Paste a headline below manually.")
    manual_title = st.text_input("Report Title:")
    manual_summary = st.text_area("Report Content:")
    if st.button("Analyze Manual Entry"):
        st.session_state['active_item'] = {"title": manual_title, "summary": manual_summary}

# 5. Dashboard Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🗞️ Captured Intel")
    if 'master_intel' in st.session_state and st.session_state['master_intel']:
        for i, item in enumerate(st.session_state['master_intel']):
            with st.container(border=True):
                st.caption(item['source'])
                st.subheader(item['title'])
                if st.button("Analyze for LinkedIn", key=f"btn_{i}"):
                    st.session_state['active_item'] = item
    else:
        st.info("System idle. Click 'Scan' or use Manual Input.")

with col2:
    st.header("🧠 Consultant Analysis")
    if 'active_item' in st.session_state:
        target = st.session_state['active_item']
        
        prompt = f"""
        Analyze as CAPO Consulting Lead:
        Topic: {target['title']}
        Summary: {target['summary']}
        
        1. Link this to Nutrition (Stunting/MDD), Social Protection (SCTP), and Emergency Response.
        2. Discuss the 'Compliance vs Ownership' risk.
        3. Draft a high-impact LinkedIn post using a professional analogy.
        """
        
        with st.spinner("AI is thinking..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
            )
            st.success("Analysis Ready!")
            st.markdown(completion.choices[0].message.content)
