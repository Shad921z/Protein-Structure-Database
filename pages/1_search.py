import streamlit as st
import sqlite3
import pandas as pd

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Protein Detail Viewer", layout="wide", page_icon="🧬")

# ================= DATABASE =================
DB_NAME = "protein_structure.db"
conn = sqlite3.connect(DB_NAME, check_same_thread=False)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1e3a8a;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .search-container {
        max-width: 600px;
        margin: 0 auto 2rem auto;
    }
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .structure-card {
        background-color: #f8fafc;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 2px solid #e2e8f0;
    }
    .image-container {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 1rem;
    }
    .section-header {
        color: #1e293b;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    .nav-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .nav-button:hover {
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# ================= PAGE TITLE =================
st.markdown('<h1 class="main-title">🧬 Protein Detail Viewer</h1>', unsafe_allow_html=True)

# ================= SEARCH INPUT =================
st.markdown('<div class="search-container">', unsafe_allow_html=True)
search_query = st.text_input("🔍 Enter PDB ID or Protein Name", placeholder="e.g., 4HHB or Hemoglobin").strip()
st.markdown('</div>', unsafe_allow_html=True)

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

    df = pd.read_sql_query(query, conn, params=(search_query, f"%{search_query}%"))

    if df.empty:
        st.error("❌ No protein found in the local database. Please contact the administrator.")
    else:
        protein = df.iloc[0]
        pdb_id = protein["pdb_id"]
        pdb_lower = pdb_id.lower()

        # ================= PROTEIN HEADER CARD =================
        st.markdown(f"""
        <div class="info-card">
            <h2 style="margin:0; font-size: 2rem;">{protein['protein_name']}</h2>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
                <strong>PDB:</strong> {pdb_id} | <strong>UniProt:</strong> {protein['uniprot_id']} | <strong>Organism:</strong> {protein['organism']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # ================= KEY METRICS =================
        st.markdown('<div class="section-header">📊 Key Metrics</div>', unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("🧬 AA Length", f"{protein['aa_length']}")
        with col2:
            st.metric("⚖️ MW (kDa)", f"{protein['molecular_weight']}")
        with col3:
            st.metric("🔬 Resolution (Å)", f"{protein['resolution']}" if protein['resolution'] else "N/A")
        with col4:
            st.metric("🧪 Method", protein['method'] if protein['method'] else "N/A")
        with col5:
            ligand_status = "✅ Yes" if protein['ligand_present'] == 1 else "❌ No"
            st.metric("💊 Ligand", ligand_status)

        # ================= STRUCTURE VISUALIZATION =================
        st.markdown('<div class="section-header">🔬 Protein Structure Visualization</div>', unsafe_allow_html=True)

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("### 🎨 Assembly Structure")
            st.markdown(f"""
            <div class="image-container">
                <img
                    src="https://cdn.rcsb.org/images/structures/{pdb_lower}_assembly-1.jpeg"
                    style="width: 100%; border-radius: 8px;"
                    alt="Assembly Structure"
                    onerror="this.onerror=null; this.src='https://via.placeholder.com/400x400?text=Image+Not+Available';"
                />
                <p style="text-align: center; color: #64748b; margin-top: 0.5rem; font-size: 0.9rem;">
                    Biological Assembly View
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            if protein['ligand_present'] == 1:
                st.markdown("### 💊 Ligand Structure")
                st.markdown(f"""
                <div class="image-container">
                    <img
                        src="https://cdn.rcsb.org/images/structures/{pdb_lower}_ligand-1.jpeg"
                        style="width: 100%; border-radius: 8px;"
                        alt="Ligand Structure"
                        onerror="this.onerror=null; this.src='https://via.placeholder.com/400x400?text=Ligand+Image+Not+Available';"
                    />
                    <p style="text-align: center; color: #64748b; margin-top: 0.5rem; font-size: 0.9rem;">
                        Bound Ligand Molecule
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("### 💊 Ligand Structure")
                st.markdown(f"""
                <div class="image-container" style="display: flex; align-items: center; justify-content: center; min-height: 300px; background: #f1f5f9;">
                    <div style="text-align: center; color: #94a3b8;">
                        <div style="font-size: 4rem; margin-bottom: 1rem;">🚫</div>
                        <h3 style="color: #64748b; margin: 0;">No Ligand Present</h3>
                        <p style="margin: 0.5rem 0 0 0;">This protein structure has no bound ligands</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # ================= BIOLOGICAL FUNCTION =================
        st.markdown('<div class="section-header">🧠 Biological Function</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="structure-card">
            <p style="font-size: 1rem; line-height: 1.6; color: #334155;">
                {protein['function']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # ================= EXTERNAL LINKS =================
        st.markdown('<div class="section-header">🔗 External Resources</div>', unsafe_allow_html=True)

        link_col1, link_col2, link_col3 = st.columns(3)

        with link_col1:
            st.markdown(f"""
            <a href="https://www.rcsb.org/structure/{pdb_id}" target="_blank" style="text-decoration: none;">
                <div style="background: #3b82f6; color: white; padding: 1rem; border-radius: 10px; text-align: center; font-weight: bold;">
                    🔬 View on RCSB PDB
                </div>
            </a>
            """, unsafe_allow_html=True)

        with link_col2:
            st.markdown(f"""
            <a href="https://www.uniprot.org/uniprotkb/{protein['uniprot_id']}" target="_blank" style="text-decoration: none;">
                <div style="background: #10b981; color: white; padding: 1rem; border-radius: 10px; text-align: center; font-weight: bold;">
                    📚 View on UniProt
                </div>
            </a>
            """, unsafe_allow_html=True)

        with link_col3:
            st.markdown(f"""
            <a href="https://www.ncbi.nlm.nih.gov/protein/?term={protein['uniprot_id']}" target="_blank" style="text-decoration: none;">
                <div style="background: #8b5cf6; color: white; padding: 1rem; border-radius: 10px; text-align: center; font-weight: bold;">
                    🧬 View on NCBI
                </div>
            </a>
            """, unsafe_allow_html=True)

        # ================= NAVIGATION =================
        st.markdown('<div class="section-header">🧭 Navigation</div>', unsafe_allow_html=True)

        nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])

        with nav_col2:
            if st.button("🎮 Open Interactive 3D Structure Viewer", use_container_width=True, type="primary"):
                st.switch_page("pages/2_3D_Structure.py")

else:
    # ================= EMPTY STATE =================
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%); border-radius: 15px; margin: 2rem 0;">
        <h2 style="color: #475569; margin-bottom: 1rem;">👋 Welcome to Protein Detail Viewer</h2>
        <p style="color: #64748b; font-size: 1.1rem; margin-bottom: 2rem;">
            Enter a PDB ID (e.g., <strong>4HHB</strong>) or protein name (e.g., <strong>Hemoglobin</strong>) to explore detailed protein information
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); max-width: 200px;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
                <strong>Key Metrics</strong>
                <p style="font-size: 0.9rem; color: #64748b; margin: 0.5rem 0 0 0;">View protein properties</p>
            </div>
            <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); max-width: 200px;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔬</div>
                <strong>3D Structures</strong>
                <p style="font-size: 0.9rem; color: #64748b; margin: 0.5rem 0 0 0;">Visualize molecular models</p>
            </div>
            <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); max-width: 200px;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧠</div>
                <strong>Functions</strong>
                <p style="font-size: 0.9rem; color: #64748b; margin: 0.5rem 0 0 0;">Learn biological roles</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.9rem; padding: 1rem;">
    Powered by RCSB PDB & UniProt | Built with Streamlit 🎈
</div>
""", unsafe_allow_html=True)