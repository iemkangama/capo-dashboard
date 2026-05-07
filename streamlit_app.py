import streamlit as st
from groq import Groq
import pandas as pd

# 1. Page Configuration & Branding
st.set_page_config(page_title="CAPO Nutrition Sentinel", page_icon="🥗")
st.title("📊 CAPO Consulting: Nutrition Sentinel")
st.markdown("""
    **Evidence-based monitoring of Malawi's Food Systems.** *Tracking nutrition outcomes through data integration and community voice.*
""")

# 2. Secure API Connection
# This reads your Groq Key from the "Secrets" we will set up in Streamlit Cloud
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("API Key not found. Please check your Streamlit Secrets.")

# 3. Data Source (Google Sheets placeholder)
# Once you have your Sheet URL, we will replace this with a live link
st.sidebar.header("Data Controls")
data_view = st.sidebar.checkbox("Show Raw Data Trends")

if data_view:
    st.info("Linking to 'CAPO_Nutrition_Data' Google Sheet...")
    # Example data to show how it will look
    df = pd.DataFrame({
        'District': ['Ntcheu', 'Phalombe', 'Mulanje', 'Thyolo'],
        'Stunting Rate (%)': [32.5, 38.1, 36.4, 34.9],
        'Risk Level': ['Stable', 'High', 'Medium', 'Medium']
    })
    st.table(df)

# 4. AI Analysis & Nutrition Outcome Prediction
st.header("🧠 Predictive Analytics")
district = st.selectbox("Select a District for Analysis:", 
                        ["Ntcheu", "Phalombe", "Mulanje", "Thyolo", "Chiradzulu"])

scenario = st.text_area("Describe the current issue (e.g., 'Maize prices increased by 20% in local markets'):")

if st.button("Generate Red Flag Alert"):
    if scenario:
        with st.spinner('AI Brain is analyzing nutrition outcomes...'):
            # This is the prompt that tells the AI to think like a Nutrition Expert
            prompt = f"""
            Analyze the following for {district}, Malawi: {scenario}.
            1. Predict the likely nutrition outcome (specifically regarding MDD and Stunting).
            2. Suggest if this is a 'Compliance' issue or a true 'Ownership' failure.
            3. Provide a 'Red Flag' summary for a LinkedIn post.
            Keep it simple for non-statisticians.
            """
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
            )
            
            st.success("Analysis Complete!")
            st.markdown("### 🚩 Alert Summary")
            st.write(completion.choices[0].message.content)
    else:
        st.warning("Please enter a scenario to analyze.")

# 5. Footer
st.divider()
st.caption("© 2026 CAPO Consulting Solutions | Data Source: NSO, WFP, & Community Pulse Checks")
