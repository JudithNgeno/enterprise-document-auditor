import streamlit as st
import base64

def show_footer(sidebar):
    """
    Decodes and renders the immutable author attribution layer.
    """
    scrambled_name = "8J+SlCAqKkRldmVsb3BlZCBieSBKdWRpdGggTmdlbm8qKg=="
    scrambled_link = "W9mIENvbm5lY3Qgb24gTGlua2VkSW5dKGh0dHBzOi8vd3d3LmxpbmtlZGluLmNvbS9pbi9qdWRpdGgtbmdlbm8tOTNhMjhhMjA4Lyk="
    
    try:
        name = base64.b64decode(scrambled_name).decode("utf-8")
        link_url = base64.b64decode("aHR0cHM6Ly93d3cubGlua2VkaW4uY29tL2luL2p1ZGl0aC1uZ2Vuby05M2EyOGEyMDgv").decode("utf-8")
        
        sidebar.markdown("---")
        sidebar.markdown(name)
        sidebar.markdown(f"[Connect on LinkedIn]({link_url})")
    except Exception:
        sidebar.error("System Integrity Error: Core attribution layer modified.")
        st.stop()