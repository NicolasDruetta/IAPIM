from pathlib import Path
import streamlit as st

# Configuración general.
st.set_page_config(page_title="IAPIM", layout="wide")
pages_dir = Path(__file__).parent / "pages"

# Obtiene dinámicamente las páginas disponibles.
def get_page_files():
    return sorted([path for path in pages_dir.glob("*.py") if not path.name.startswith("_")], key=lambda path: path.name.lower())

# Página principal.
def show_main():
    st.title("IAPIM")
    for page_file in get_page_files():
        st.page_link(f"pages/{page_file.name}", label=page_file.name)

# Menú general.
page_files = get_page_files()
menu_pages = [st.Page(show_main, title="main.py", default=True)]
menu_pages.extend(st.Page(f"pages/{page_file.name}", title=page_file.name) for page_file in page_files)
st.markdown("<style>[data-testid='stSidebarNav']::before{content:'Menú';display:block;font-size:1.75rem;font-weight:700;margin:0 1rem 1rem 1rem;}</style>", unsafe_allow_html=True)
navigation = st.navigation(menu_pages, position="sidebar")
navigation.run()