try:
    import libreselect_foot_v03_streamlit  # noqa: F401
except Exception as exc:
    import streamlit as st

    st.set_page_config(page_title="LibreSelect Foot", page_icon="⚽", layout="wide")
    st.title("⚽ LibreSelect Foot v0.3")
    st.markdown("**L'outil le plus perfectionné pour les sélections nationales de football**")
    st.warning("Le fichier principal n'a pas pu être chargé.")
    st.info("Vérifiez que `libreselect_foot_v03_streamlit.py` est présent et que ses dépendances sont installées.")
    st.code(f"Erreur: {exc}")
