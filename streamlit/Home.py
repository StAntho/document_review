import streamlit as st
from dotenv import load_dotenv
import os, tempfile, requests
from pathlib import Path
import pandas as pd

# === Init session state ===
if "analyse_done" not in st.session_state:
    st.session_state.analyse_done = False
if "extraction_response" not in st.session_state:
    st.session_state.extraction_response = None

param2 = "./markdown"

# === API ===
load_dotenv()
URL_ANALYSE_API = f"{os.getenv('STREAMLIT_URL_API')}document_analyser/upload"
URL_SEARCH_API = f"{os.getenv('STREAMLIT_URL_API')}document_analyser/search"
HEADERS = {
    "X-API-Key": os.getenv('SECURITY_API_KEY')
}

st.set_page_config(
    page_title="Analyse_doc",
    page_icon="📄",
)
st.title("Analyse Document 📄")

document = st.file_uploader("Upload your document", type=['pdf'])

if document and st.button("Lancer l'extraction"):
    st.session_state.extraction_done = False

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

            with open(tmp_path, "rb") as f:
                response = requests.post(
                    URL_ANALYSE_API,
                    files={"file": (document.name, f, "application/pdf")},
                    headers=HEADERS
                )

            st.session_state.tmp_name = tmp_path

            if response.status_code == 200:
                st.session_state.extraction_response = response.json()
                st.write(response.json())
                st.session_state.extraction_done = True

                st.session_state.key_dates = None

            else:
                st.session_state.extraction_response = None
                st.error(f"Erreur {response.status_code} : {response.text}")

    if st.session_state.extraction_response:
        result = st.session_state.extraction_response

        st.markdown(f"**Fichier :** `{result['path']}` — **Format détecté :** `{result['format']}`")

        st.markdown(f"#### 📑 Chunks fait ({len(result['chunks'])})")
        if result["chunks"]:
            df = pd.DataFrame(result["chunks"])
            st.dataframe(df, use_container_width=True)
        else:
            st.write("Aucun chunk extrait.")

        
        st.markdown("#### 🔍 Recherche dans le document")
        search_query = st.text_input("Rechercher un mot ou une expression")

        if search_query:
            search_response = requests.post(
                URL_SEARCH_API,
                json={"chunks": result["chunks"], "query": search_query},
                headers=HEADERS
            )

            if search_response.status_code != 200:
                st.error(f"Erreur {search_response.status_code} : {search_response.text}")
            else:
                search_results = search_response.json()["results"]
                st.write(f"{len(search_results)} résultat(s) pour « {search_query} »")

                CONTEXT_LABELS = {
                    "table": "📊 Tableau",
                    "section": "🏷️ Titre + contenu",
                    "paragraph": "📝 Paragraphe",
                }

                for res in search_results:
                    match = res["match"]
                    label = CONTEXT_LABELS.get(res["context_type"], res["context_type"])
                    with st.expander(f"{label} — page {match['page']} — « {match['content'][:80]} »", expanded=False):
                        for chunk in res["context"]:
                            if chunk["type"] == "table":
                                st.write(chunk["content"])
                            elif chunk["type"] in ("title", "subtitle", "heading"):
                                st.markdown(f"**{chunk['content']}**")
                            else:
                                st.write(chunk["content"])
