import streamlit as st

st.set_page_config(
    page_title="Protein Structure Database",
    layout="wide"
)

# ================= HEADER =================

st.title("🧬 Protein Structure Database")
st.subheader("An interactive platform to explore protein 3D structures")

st.write(
    """
    This application provides an interactive interface to **store, search, and visualize protein structures**
    using publicly available biological databases such as **RCSB PDB**, **NCBI**, and **PubChem**.

    The platform is designed for **students, educators, and beginners in bioinformatics** who want a
    clean and intuitive way to explore protein structures without dealing with complex file formats.
    """
)

st.divider()

# ================= FEATURES =================

st.subheader("✨ Key Features")

st.markdown("""
- 🔍 **Search proteins** using PDB IDs
- 🧬 **Interactive 3D visualization** of protein structures
- 🧪 **Ligand molecular structure display** (via PubChem)
- 🔐 **Admin-controlled data ingestion**
- 📊 **Structured protein database** for easy access
""")

st.divider()

# ================= WHO IS THIS FOR =================

st.subheader("👩‍🔬 Who is this for?")

st.markdown("""
- **Life science students** learning structural biology
- **Beginners in bioinformatics**
- **Educators** demonstrating protein structures
- **Developers** building biology-focused applications
""")

st.divider()

# ================= NAVIGATION =================

st.subheader("🚀 Get Started")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔍 Search Protein"):
        st.switch_page("pages/3_Search.py")

with col2:
    if st.button("🧬 3D Structure Viewer"):
        st.switch_page("pages/2_3D_Structure.py")

with col3:
    if st.button("🔐 Admin Panel"):
        st.switch_page("pages/1_Admin.py")

st.divider()

# ================= FOOTER =================

st.caption(
    "📌 Data sources: RCSB PDB, NCBI iCn3D, PubChem | Built using Python & Streamlit"
)
