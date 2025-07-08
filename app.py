import streamlit as st
import requests

# --- API URLs ---
API_GENERATE_URL = "https://ny97l1bvp2.execute-api.us-east-1.amazonaws.com/v1/generate"
API_HISTORY_URL = "https://ny97l1bvp2.execute-api.us-east-1.amazonaws.com/v1/history"

# --- Page config ---
st.set_page_config(page_title="AI Content Generator", layout="wide")

# --- Header ---
st.title("AI Content Generator")
st.write("Enter keywords to get AI-generated creative content.")

# --- Content Generation Form ---
with st.form("generate_form"):
    keywords = st.text_input("Enter keywords or short description")
    submit = st.form_submit_button("Generate")

if submit and keywords.strip():
    with st.spinner("Generating..."):
        try:
            response = requests.post(API_GENERATE_URL, json={"keywords": keywords})
            if response.status_code == 200:
                result = response.json().get("result") or response.json().get("GeneratedContent")
                st.success("Generated Content:")
                st.write(result)
            else:
                st.error(f"Failed to generate content.\n\nStatus code: {response.status_code}\n\nMessage: {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")

# --- Fetch History ---
@st.cache_data(ttl=60)
def fetch_history():
    try:
        response = requests.get(API_HISTORY_URL)
        if response.status_code == 200:
            items = response.json().get("items", [])
            return sorted(items, key=lambda x: x.get("Timestamp", ""), reverse=True)
        return []
    except Exception as e:
        st.error(f"Error fetching history: {e}")
        return []

history_items = fetch_history()

# --- Sidebar: History Titles ---
st.sidebar.header("📜 Your History")
if not history_items:
    st.sidebar.info("No history yet.")
    selected_title = None
else:
    titles = [item.get('InputKeywords', 'N/A') for item in history_items]
    selected_title = st.sidebar.radio("Select a past input", titles)

# --- Main Display: Selected History ---
if selected_title:
    selected_item = next(
        (item for item in history_items if item.get('InputKeywords') == selected_title),
        None
    )
    if selected_item:
        st.markdown("---")
        st.subheader(f"📄 History: {selected_item.get('InputKeywords')}")
        st.markdown(f"**Input:** {selected_item.get('InputKeywords')}")
        st.markdown("**Generated Content:**")
        st.write(selected_item.get("GeneratedContent"))
        st.caption(f"Model: {selected_item.get('ModelUsed')} | ID: {selected_item.get('Id')}")
