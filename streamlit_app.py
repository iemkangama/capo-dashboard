import streamlit as st
from groq import Groq
import feedparser
from bs4 import BeautifulSoup

# 1. Branding & Header
st.set_page_config(page_title="CAPO Sentinel", layout="wide")
st.title("📡 CAPO Sentinel: Automated Intelligence")
st.markdown("---")

# 2. Connection
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Sentinel Engine: The Scraper
def fetch_malawi_news():
    # Feeds for ReliefWeb (UNICEF/WFP) and Malawi News
    feeds = [
        "https://reliefweb.int/country/mwi/rss.xml",
        "https://www.google.com/alerts/feeds/14716766023348123456/123456" # Placeholder for a custom alert
    ]
    all_news = []
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]: # Take top 5 latest
            all_news.append({"title": entry.title, "link": entry.link, "summary": entry.summary})
    return all_news

# 4. Sidebar: Dashboard Controls
st.sidebar.header("Sentinel Controls")
if st.sidebar.button("🔍 Scan for Emerging Issues"):
    news_items = fetch_malawi_news()
    st.session_state['news'] = news_items

# 5. Main Display
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🗞️ Latest Captured Intelligence")
    if 'news' in st.session_state:
        for item in st.session_state['news']:
            with st.expander(item['title']):
                st.write(item['summary'])
                if st.button(f"Analyze for LinkedIn", key=item['title']):
                    st.session_state['selected_issue'] = item['title'] + " - " + item['summary']
    else:
        st.info("Click 'Scan' in the sidebar to hunt for data.")

with col2:
    st.header("🧠 Nutrition Outcome Analysis")
    if 'selected_issue' in st.session_state:
        issue = st.session_state['selected_issue']
        
        prompt = f"""
        Analyze this Malawi news/report: {issue}
        1. Link to specific Nutrition Outcomes (Stunting, Wasting, or MDD).
        2. Identify if this is a 'Compliance' or 'Ownership' risk.
        3. Draft a LinkedIn post for CAPO Consulting that uses simple language and a visual description of a trend.
        """
        
        with st.spinner("Linking to nutrition outcomes..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
            )
            st.success("Draft Analysis Ready!")
            st.markdown(completion.choices[0].message.content)

# 6. Easy-to-Understand Visuals (Placeholder)
st.markdown("---")
st.subheader("📊 Trend Visualization")
st.write("Visualizations will appear here once local market data is synced.")
