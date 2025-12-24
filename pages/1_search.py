import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image

# ================= DATABASE =================

DB_NAME = "protein_structure.db"
conn = sqlite3.connect(DB_NAME, check_same_thread=False)

# ================= PAGE TITLE =================

st.title("🧬 Protein Detail Viewer")


# ================= SEARCH INPUT =================

search_query = st.text_input("Enter PDB ID or Protein Name").strip()

if search_query:

    query = """
    SELECT
        p.protein_name,
        p.pdb_id,
        p.uniprot_id,
        p.organism,
        p.function,
        p.aa_length,
        p.molecular_weight,
        s.method,
        s.resolution,
        s.ligand_present
    FROM protein p
    JOIN protein_structure s ON p.protein_id = s.protein_id
    WHERE LOWER(p.pdb_id) = LOWER(?)
       OR LOWER(p.protein_name) LIKE LOWER(?)
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(search_query, f"%{search_query}%")
    )

    if df.empty:
        st.error("No protein found in the local Database, Contact the administrator.")
    else:
        protein = df.iloc[0]

        # ================= BASIC INFO =================
        st.subheader("🧬 Protein Summary")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("AA Length", protein["aa_length"])
        c2.metric("MW (kDa)", protein["molecular_weight"])
        c3.metric("Resolution (Å)", protein["resolution"])

        st.divider()

        st.subheader("🔬 Identity & Function")

        st.markdown(f"""
        - **Protein Name:** {protein['protein_name']}
        - **PDB ID:** `{protein['pdb_id']}`
        - **UniProt ID:** `{protein['uniprot_id']}`
        - **Organism:** {protein['organism']}
        """)

        st.subheader("🧠 Biological Function")
        st.write(protein["function"])

      # ===== lowercase PDB ID =====
    pdb_id = protein["pdb_id"]
    pdb_lower = pdb_id.lower()

    st.subheader("📸 Protein Structure")

    image_html = f"""
    <div style="
        background-color: #f9fafb;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        text-align: center;
    ">
        <img
            src="https://cdn.rcsb.org/images/structures/{pdb_lower}_assembly-1.jpeg"
            style="max-width: 100%; border-radius: 10px;"
        />
        <p style="margin-top: 8px; color: #555; font-size: 14px;">
            PDB Structure Image: {pdb_id}
        </p>
    </div>
    """

    st.markdown(image_html, unsafe_allow_html=True)

    st.divider()


else:
    st.info("Enter a protein name or PDB ID to view details.")

    #========== BUTTONS =============

    st.markdown("------")

    st.set_page_config(page_title="Protein DB", layout="wide")


    st.subheader("Navigate")

    col1, = st.columns(1)


    with col1:
        if st.button("🧬 3D Structure Viewer"):
            st.switch_page("pages/2_3D_Structure.py")


