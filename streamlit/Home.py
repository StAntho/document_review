import streamlit as st
from dotenv import load_dotenv
import os, tempfile, requests
from pathlib import Path

# === Init session state ===
if "analyse_done" not in st.session_state:
    st.session_state.analyse_done = False


param2 = "./markdown"

# === API ===
load_dotenv()
URL_ANALYSE_API = f"{os.getenv('STREAMLIT_URL_API')}"
HEADERS = {
    "X-API-Key": os.getenv('SECURITY_API_KEY')
}

st.set_page_config(
    page_title="Analyse_doc",
    page_icon="📄",
)
st.title("Analyse Document 📄")

document = st.file_uploader("Upload your document", type=['pdf'])

if document:
    st.write(f"📥 Fichier téléchargé: {document}")

    if not st.session_state.analyse_done:
        with st.status("Analyse en cours...", expanded=True) as status:
            st.write("Sauvegarde du fichier...")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(document.read())
                tmp_path = tmp.name

            filename = Path(tmp_path).stem
            st.write(filename)
            st.session_state.md_dir = f"{param2}/{filename}"

            st.write("Fichier sauvegardé :", tmp_path)
            st.write("Analyse du fichier...")
