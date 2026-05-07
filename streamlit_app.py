import streamlit as st
from groq import Groq

# 1. Page Setup & National Benchmarks
st.set_page_config(page_title="CAPO Master Sentinel", layout="wide")
st.title("📡 CAPO Consulting: Strategic Sentinel")

# --- 📊 NATIONAL BENCHMARK DATA (2026) ---
with st.expander("📊 View National Nutrition Benchmarks (Official NNIS/SUN Mirror)", expanded=False):
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Stunting (National)", "37.6%", "+0.5% reversal")
    col_b.metric("Wasting (U5)", "2.0%", "-2.9% improvement")
    col_c.metric("SCTP Reach", "303k HH", "Mtukula Pakhomo")
    st.info("⚠️ Hotspot Alert: Chitipa (50.8%) & Neno (50.0%) stunting rates.")

# 2. Connection
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Sidebar Intelligence Controls
with st.sidebar:
    st.header("Intelligence Input")
    topic = st.text_input("Enter Topic (e.g. 'Neno floods' or 'SCTP delays')")
    context = st.text_area("Paste Report Text/Headline here:")
    analyze_btn = st.button("Generate Linked Narrative")

# 4. Main Analysis Engine
if analyze_btn:
    # We pass the official benchmarks INTO the prompt so the AI is 'Data-Aware'
    master_prompt = f"""
    You are the Lead Consultant at CAPO. Use these 2026 Malawi Benchmarks:
    - Stunting: 37.6% (Reversing)
    - Wasting: 2.0% (Target Met)
    - Crisis: IPC Phase 3 in Southern Region (May 2026)
    
    Current Issue: {topic}
    Report Data: {context}
    
    TASK:
    1. THE NARRATIVE: Compare the 'Current Issue' to the 'National Benchmarks'. 
       Does this event threaten the 2.0% wasting target or worsen the 37.6% stunting?
    2. PROJECT MGMT: Is this a failure of 'Compliance' (doing things right) or 'Ownership' (doing the right things)?
    3. SOCIAL PROTECTION: How should the SCTP 'Mtukula Pakhomo' respond to this shock?
    4. LINKEDIN DRAFT: Write a post using a 'Data Visualization' hook (e.g., 'The gap between 2% and 37%').
    """
    
    with st.spinner("Linking to National Information Systems..."):
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": master_prompt}],
        )
        
        # Display the Narrative
        st.header("🧠 CAPO Strategic Narrative")
        st.markdown(completion.choices[0].message.content)
else:
    st.info("👈 Enter a topic in the sidebar to generate a data-backed narrative.")
