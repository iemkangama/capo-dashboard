import streamlit as st
from groq import Groq
import feedparser
import requests
from PIL import Image

# 1. PAGE SETUP
st.set_page_config(page_title="CAPO Master Sentinel: Research Edition", layout="wide")

# 2. BRANDING
try:
    logo = Image.open("Capo_Consulting_Logo.png") 
    col_l, col_r = st.columns([1, 6])
    with col_l: st.image(logo, width=120)
    with col_r:
        st.title("CAPO Consulting: Research Sentinel")
        st.markdown("### *Malawi & SADC Regional Evidence Hub*")
except:
    st.title("📡 CAPO Consulting: Research Sentinel")

# 3. RESEARCH ENGINE LOGIC
def fetch_academic_intel():
    # Academic-specific sources (Journals & Technical Policy Briefs)
    research_feeds = [
        {"name": "Malawi Medical Journal (MMJ)", "url": "https://www.mmj.mw/feed/"},
        {"name": "IFPRI/LUANAR Research", "url": "https://massp.ifpri.info/feed/"},
        {"name": "ZEF/GIZ Nutrition Briefs", "url": "https://reliefweb.int/organization/giz/rss.xml"},
        {"name": "SADC IPC Research (FAO)", "url": "https://reliefweb.int/organization/fao/rss.xml?country=146"}
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    research_bank = []
    
    for feed in research_feeds:
        try:
            resp = requests.get(feed['url'], headers=headers, timeout=10)
            parsed = feedparser.parse(resp.content)
            for entry in parsed.entries[:5]:
                # FILTER: Only keep papers relevant to Nutrition or Social Protection
                keywords = ['nutrition', 'stunting', 'wasting', 'food', 'SCTP', 'diet', 'agriculture']
                if any(key in entry.title.lower() or key in entry.get('summary', '').lower() for key in keywords):
                    research_bank.append({
                        "title": entry.title,
                        "summary": entry.get('summary', 'Academic study available.'),
                        "source": feed['name'],
                        "link": entry.link
                    })
        except: continue
    return research_bank

# 4. SIDEBAR CONTROLS
with st.sidebar:
    st.header("Intelligence Controls")
    if st.button("🎓 SCAN ACADEMIC RESEARCH", use_container_width=True):
        st.session_state['research_data'] = fetch_academic_intel()
    
    st.divider()
    st.subheader("Regional Context (2026)")
    st.caption("National Stunting: 37.6%")
    st.caption("SADC Avg: 30.3%")

# 5. DASHBOARD DISPLAY
col_left, col_right = st.columns([1, 1])

with col_left:
    st.header("📑 Research & Evidence")
    if 'research_data' in st.session_state and st.session_state['research_data']:
        for i, item in enumerate(st.session_state['research_data']):
            with st.container(border=True):
                st.write("📖 **PEER-REVIEWED / TECHNICAL**")
                st.subheader(item['title'])
                st.caption(f"Source: {item['source']}")
                if st.button("Analyze Research Impact", key=f"res_{i}"):
                    st.session_state['active_res'] = item
    else:
        st.info("Click the Academic Scan button to pull the latest 2026 research papers.")

with col_right:
    st.header("🧠 CAPO Evidence Synthesis")
    if 'active_res' in st.session_state:
        target = st.session_state['active_res']
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        prompt = f"""
        Role: Senior Research Consultant at CAPO.
        Task: Synthesize this Academic Research for a non-technical NGO Director.
        
        Research Title: {target['title']}
        Abstract/Summary: {target['summary']}
        
        Analysis Requirements:
        1. THE DATA: How does this change our understanding of Malawi's 37.6% stunting reversal?
        2. OWNERSHIP: How can academic findings be translated into 'Ownership' at the district level?
        3. SADC LINK: Does this finding apply to our neighbors (Zambia/Mozambique)?
        4. LINKEDIN POST: Write a post that starts with "The data just changed..." or "Evidence shows..."
        """
        
        with st.spinner("Synthesizing evidence..."):
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
            st.markdown(res.choices[0].message.content)
            st.link_button("Read Original Paper", target['link'])
