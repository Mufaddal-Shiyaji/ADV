import streamlit as st
import pandas as pd
from utils import generate_visualizations, get_gemini_response_multiple, parse_gemini_response_multiple, get_gemini_response, parse_gemini_response

# Set up Google Gemini API key
GENAI_API_KEY = "AIzaSyD4eCbLmYYDOK3SCDDrcPFeCU0ZMcMjarQ"  # Replace with your actual Gemini API key

# Streamlit page configuration
st.set_page_config(
    page_title="EasyDV - AI-Powered Data Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar for navigation and styling
st.sidebar.title("📊 **EasyDV**")
st.sidebar.markdown("""
Welcome to **EasyDV**, your AI-powered assistant for data visualization and insights. 
Upload your dataset to get started!
""")

# Sidebar instructions
st.sidebar.subheader("Steps to Get Started:")
st.sidebar.markdown("""
1. Upload your CSV file.  
2. Preview the dataset.  
3. Ask questions about the data or let EasyDV suggest visualizations.
""")

# Main title and description
st.title("🎨 **EasyDV: Data Visualization and Insights**")
st.markdown("""
Streamline your data analysis process with **EasyDV**. Effortlessly upload datasets, generate insightful visualizations, 
and ask natural language questions to uncover hidden patterns.
""")

# File upload section
uploaded_file = st.file_uploader("📂 Upload a CSV file", type="csv")
if uploaded_file is not None:
    # Load dataset
    df = pd.read_csv(uploaded_file)
    st.markdown("### 📋 **Dataset Preview**")
    st.dataframe(df.head(), width=1000)

    # Generate AI-suggested visualizations on the right
    if "ai_visualizations" not in st.session_state:
        with st.spinner("Generating AI-powered visualizations..."):
            response = get_gemini_response_multiple(df, GENAI_API_KEY)
            visualizations = parse_gemini_response_multiple(response)
            st.session_state["ai_visualizations"] = visualizations

    # Create two columns for layout
    col1, col2 = st.columns(2)

    # Left: Natural language query section
    with col1:
        st.markdown("### 🤔 **Ask a Question About the Data**")
        query = st.text_input("Type your question here:")
        if query:
            # Get response from Gemini model
            with st.spinner("Generating insights..."):
                response = get_gemini_response(query, df, GENAI_API_KEY)
                if response:
                    try:
                        chart_type, chart_code, x_label, y_label = parse_gemini_response(response)
                        st.success("✅ Insight Generated!")
                        st.markdown(f"#### 🔍 **Gemini's Answer:**\n{chart_type}")
                        generate_visualizations(df, chart_type, chart_code, x_label, y_label)
                        st.markdown(f"#### ℹ️ **Explanation**:\nThis is a {chart_type.lower()} visualization showing the relationship between `{x_label}` and `{y_label}`.")
                    except Exception as e:
                        st.error("Error while generating the visualization. Please try again.")
                else:
                    st.error("No response received from the AI. Please check your query.")

    # Right: Fixed AI-generated visualizations
    with col2:
        st.markdown("### 🧠 **AI-Generated Visualizations**")
        st.write("Here are automatically generated insights and visualizations based on your dataset:")
        for idx, (chart_type, chart_code, x_label, y_label) in enumerate(st.session_state["ai_visualizations"]):
            st.markdown(f"#### 📊 Visualization {idx + 1}: {chart_type}")
            generate_visualizations(df, chart_type, chart_code, x_label, y_label)
            st.markdown("---")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("© 2024 **EasyDV** | Empowered by Gemini.")
