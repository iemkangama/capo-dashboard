import streamlit as st
from groq import Groq
import feedparser

# 1. Page Branding
st.set_page_config(page_title="CAPO Sentinel", layout="wide")
st.title("📡 CAPO Sentinel: Automated Intelligence")
st.markdown("---")

# 2. Connection
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Enhanced Scraper with working Malawi Feeds
def fetch_malawi_news():
    # Using specific ReliefWeb and UN feeds for Malawi
    feeds = [
        "https://reliefweb.int/country/mwi/rss.xml", # UNICEF, WFP, FAO updates
        "https://www.un.org/sustainabledevelopment/feed/", # Global goals including Zero Hunger
    ]
    all_news = []
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:8]: # Take latest 8 items
                all_news.append({
                    "title": entry.title, 
                    "link": entry.link, 
                    "summary": entry.get('summary', 'No summary available.')
                })
        except Exception as e:
            st.error(f"Error fetching {url}: {e}")
    return all_news

# 4. Sidebar: Scan Button
st.sidebar.header("Sentinel Controls")
scan_clicked = st.sidebar.button("🔍 Scan for Emerging Issues")

# 5. Main Layout
col1, col2 = st.columns([1, 1])

# LOGIC: If button is clicked, fetch news and store it
if scan_clicked:
    with st.spinner("Hunting for news across UN, WFP, and FAO..."):
        st.session_state['news_list'] = fetch_malawi_news()

# col1: Display the news
with col1:
    st.header("🗞️ Captured Intelligence")
    if 'news_list' in st.session_state and st.session_state['news_list']:
        for i, item in enumerate(st.session_state['news_list']):
            # Display news in an easy-to-read box
            with st.container(border=True):
                st.subheader(item['title'])
                # Clean up HTML tags in summary
                summary_text = item['summary'][:300] + "..." 
                st.write(summary_text)
                
                # Button to select THIS news for analysis
                if st.button(f"Analyze for LinkedIn", key=f"btn_{i}"):
                    st.session_state['selected_context'] = f"TITLE: {item['title']} \nSUMMARY: {item['summary']}"
    else:
        st.info("No data captured yet. Please click the 'Scan' button in the sidebar.")

# col2: AI Analysis
with col2:
    st.header("🧠 Nutrition Outcome Analysis")
    if 'selected_context' in st.session_state:
        context = st.session_state['selected_context']
        
        with st.spinner("AI Brain is linking indicators to outcomes..."):
            prompt = f"""
            You are a nutrition expert at CAPO Consulting. Analyze this news:
            {context}
            
            1. Link this to a NUTRITION OUTCOME (e.g. Stunting, MDD, Wasting).
            2. Is this a Project Management 'Compliance' trap or an 'Ownership' opportunity?
            3. Write a LinkedIn post draft that uses a simple visual analogy (like a plate or a shadow).
            """
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
            )
            st.success("Analysis Ready for CAPO Consulting!")
            st.markdown(completion.choices[0].message.content)
    else:
        st.write("Select a news item from the left to start the LinkedIn analysis.")
