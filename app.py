import streamlit as st
import os
from core.pipeline import DocumentAuditorEngine

st.set_page_config(page_title="Document Auditor & Compliance Engine", page_icon="🛡️", layout="wide")

st.title("🛡️ Enterprise Document Auditor")
st.caption("Automated format routing, semantic multi-format ingestion, and localized data validation matrix.")

# Dual-Mode credential verification
openai_api_key = st.secrets.get("OPENAI_API_KEY", "")

sidebar = st.sidebar
sidebar.header("System Access Controls")

if not openai_api_key:
    openai_api_key = sidebar.text_input(
        "Enter Your OpenAI API Key:", 
        type="password", 
        help="Access token is stored entirely in memory cache and never tracked."
    )
    if not openai_api_key:
        st.info(" System offline. Provide a valid authorization string in the sidebar panel to initialize database connections.")
        st.stop()

# Initialize detached business engine using verified credentials
engine = DocumentAuditorEngine(api_key=openai_api_key)

sidebar.markdown("---")
sidebar.subheader("Ingestion Management")
uploaded_file = sidebar.file_uploader(
    "Ingest Source Documentation File", 
    type=["pdf", "docx", "txt", "csv"]
)

if uploaded_file:
    # Build explicit runtime stream storage to read file contents cleanly
    temp_path = f"sys_stream_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    try:
        # Cache database index arrays across internal operational triggers
        if "vector_index" not in st.session_state:
            with st.spinner("Processing documents into vectorized operational states..."):
                st.session_state.vector_index = engine.process_document(temp_path)
                st.success("Target context pipeline established successfully.")

        st.subheader("Analysis Terminal")
        user_query = st.text_input("Enter structural audit inquiry or targeted extraction query:")
        
        if user_query:
            with st.spinner("Scanning vectorized indexing metrics..."):
                execution_payload = engine.execute_audit_query(
                    st.session_state.vector_index, 
                    user_query
                )
                
                st.markdown("###  Engine Findings")
                st.info(execution_payload["answer"])
                
                with st.expander(" Audited Source References"):
                    for reference in execution_payload["context"]:
                        source_page = reference.metadata.get("page", 0) + 1
                        st.markdown(f"**Data Segment Reference Matrix — Section/Page {source_page}:**")
                        st.caption(reference.page_content)
                        st.markdown("---")
                        
    except Exception as error:
        st.error(f"Execution pipeline exception: {str(error)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
else:
    if "vector_index" in st.session_state:
        del st.session_state.vector_index
    st.info("Awaiting structural document stream execution via ingestion panel.")

sidebar.markdown("---")
sidebar.markdown("**Developed by [Judith Ngeno]**")
sidebar.sidebar_link("🔗 Connect on LinkedIn", url="https://www.linkedin.com/in/judith-ngeno-93a28a208/")    