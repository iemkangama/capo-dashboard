import streamlit as st
from groq import Groq
import feedparser

# 1. Branding: Professional Emergency Focus
st.set_page_config(page_title="CAPO Emergency Sentinel", layout="wide")
st.title("🚨 CAPO Sentinel: Nutrition in Emergencies (NiE)")
st.markdown("""
    **Rapid Response Monitoring:** *Tracking IPC Outcomes, SAM/MAM Trends, and Humanitarian Logistics in Malawi.*
""")

# 2. Connection
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Emergency-Specific Keywords
TECHNICAL_KEYWORDS = [
    "nutrition in emergency", "NiE", "emergency response", "IPC Phase", 
    "SAM", "MAM", "wasting", "humanitarian", "relief", "flood", "cholera",
    "lean season", "SCTP", "cash transfer", "WFP", "UNICEF", "DREF"
]

# 4. Emergency Scraper
def fetch_emergency_intel():
    feeds = [
        "https://reliefweb.int/country/mwi/rss.xml", # The gold standard for SitReps
        "https://fews.net/southern-africa/malawi/rss.xml", # Food Security Outlooks
        "https://www.unicef.org/malawi/stories/feed" # Child nutrition on the ground
    ]
    emergency_data = []
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                content = (entry.title + entry.get('summary', '')).lower()
                if any(key in content for key in TECHNICAL_KEYWORDS):
                    emergency_data.append({
                        "title": entry.title,
                        "link": entry.link,
                        "summary": entry.get('summary', 'Detailed situation report.')
                    })
        except: continue
    return emergency_data

# 5. Dashboard UI
if st.sidebar.button("📡 Deploy Emergency Scan"):
    st.session_state['emergency_intel'] = fetch_emergency_intel()

col1, col2 = st.columns([1, 1])

with col1:
    st.header("⚠️ Live Emergency Alerts")
    if 'emergency_intel' in st.session_state and st.session_state['emergency_intel']:
        for i, item in enumerate(st.session_state['emergency_intel'][:10]):
            with st.container(border=True):
                st.warning(f"ALERT: {item['title']}")
                if st.button("Analyze Crisis Linkage", key=f"btn_em_{i}"):
                    st.session_state['active_emergency'] = item
    else:
        st.info("No active emergency alerts captured. Run scan.")

with col2:
    st.header("🧠 NiE Strategic Analysis")
    if 'active_emergency' in st.session_state:
        target = st.session_state['active_emergency']
        
        prompt = f"""
        Analyze this as a Senior Nutrition in Emergencies (NiE) Consultant for CAPO:
        Issue: {target['title']}
        Summary: {target['summary']}
        
        1. CRISIS IMPACT: How does this specific emergency (e.g. flood/drought) trigger Acute Malnutrition (Wasting)?
        2. RESPONSE GAP: What is the risk of 'Compliance-only' response vs 'Local Ownership' in this emergency?
        3. SOCIAL PROTECTION LINK: How should Social Cash Transfers be adjusted for this specific shock (SRSP)?
        4. LINKEDIN POST: Write a thought-leadership post. 
           Analogy: Use 'The Emergency Room' vs 'The Wellness Clinic' to explain why we must act now.
        """
        
        with st.spinner("Analyzing emergency data points..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
            )
            st.success("NiE Strategy Drafted!")
            st.markdown(completion.choices[0].message.content)
