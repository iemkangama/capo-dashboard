import streamlit as st
from groq import Groq
import feedparser

# 1. Page Branding - Unified for CAPO Consulting
st.set_page_config(page_title="CAPO Master Sentinel", layout="wide")
st.title("📡 CAPO Consulting: Master Sentinel")
st.markdown("""
    **Integrated Intelligence:** *Nutrition (Specific/Sensitive), Social Protection (SCTP), and Emergency Response (NiE).*
""")

# 2. Connection
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Master Technical Keywords
TECHNICAL_KEYWORDS = [
    "nutrition", "stunting", "wasting", "food systems", "SUN", "dietary diversity",
    "social protection", "cash transfer", "SCTP", "safety net",
    "emergency", "humanitarian", "IPC Phase", "SAM", "MAM", "flood", "drought"
]

# 4. Master Scraper
def fetch_master_intel():
    feeds = [
        "https://reliefweb.int/country/mwi/rss.xml", 
        "https://scalingupnutrition.org/news/feed",
        "https://fews.net/southern-africa/malawi/rss.xml",
        "https://www.worldbank.org/en/country/malawi/news/rss"
    ]
    all_data = []
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                content = (entry.title + entry.get('summary', '')).lower()
                if any(key in content for key in TECHNICAL_KEYWORDS):
                    # Tagging the news type based on keywords
                    category = "Nutrition"
                    if any(x in content for x in ["cash", "sctp", "protection"]): category = "Social Protection"
                    if any(x in content for x in ["emergency", "ipc", "sam", "flood"]): category = "Emergency (NiE)"
                    
                    all_data.append({
                        "title": entry.title,
                        "category": category,
                        "summary": entry.get('summary', 'Detailed report available.'),
                        "link": entry.link
                    })
        except: continue
    return all_data

# 5. Sidebar Controls
st.sidebar.header("Sentinel Controls")
if st.sidebar.button("🔍 Run Full System Scan"):
    st.session_state['master_intel'] = fetch_master_intel()

# 6. Dashboard Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🗞️ Captured Intelligence")
    if 'master_intel' in st.session_state:
        # Filter by Category in the UI
        cat_filter = st.selectbox("Filter by Subject:", ["All", "Nutrition", "Social Protection", "Emergency (NiE)"])
        
        for i, item in enumerate(st.session_state['master_intel']):
            if cat_filter == "All" or item['category'] == cat_filter:
                with st.container(border=True):
                    st.caption(f"Category: {item['category']}")
                    st.subheader(item['title'])
                    if st.button("Analyze for LinkedIn", key=f"btn_{i}"):
                        st.session_state['active_item'] = item
    else:
        st.info("System idle. Click 'Run Full System Scan' to begin.")

with col2:
    st.header("🧠 Consultant Analysis")
    if 'active_item' in st.session_state:
        target = st.session_state['active_item']
        
        prompt = f"""
        Analyze as CAPO Consulting Lead:
        Topic: {target['title']}
        Category: {target['category']}
        
        1. THE LINK: How does this connect Nutrition, Social Protection, and Emergency Response?
        2. PM/CHANGE: Discuss the 'Compliance vs Ownership' risk for this specific update.
        3. DATA TREND: What specific indicator should we watch (e.g. Maize price, Stunting rate, SCTP reach)?
        4. LINKEDIN POST: Write a professional post that links all three subjects.
        """
        
        with st.spinner("Synthesizing multi-sectoral data..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
            )
            st.success("Master Analysis Ready!")
            st.markdown(completion.choices[0].message.content)
