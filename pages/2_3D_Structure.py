import streamlit as st
import streamlit.components.v1 as components

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="3D Structure Viewer",
    layout="wide",
    page_icon="🧬",
    initial_sidebar_state="collapsed"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Main container styling */
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    /* Search container */
    .search-container {
        max-width: 700px;
        margin: 0 auto 2rem auto;
        padding: 2rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 2px solid #e2e8f0;
    }

    /* Input styling */
    .stTextInput > div > div > input {
        font-size: 1.2rem;
        padding: 1rem;
        border-radius: 12px;
        border: 2px solid #cbd5e1;
        text-align: center;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    /* Viewer container */
    .viewer-container {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        border: 3px solid #1e293b;
        background: #0f172a;
        margin: 2rem 0;
    }

    /* Info cards */
    .info-card {
        background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #e2e8f0;
        margin-bottom: 1rem;
    }

    .feature-badge {
        display: inline-block;
        background: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.9rem;
        color: #475569;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        max-width: 900px;
        margin: 2rem auto;
    }

    .popular-structures {
        margin-top: 3rem;
        padding: 1.5rem;
        background: white;
        border-radius: 15px;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown('<h1 class="main-title">🧬 Interactive 3D Structure Viewer</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explore protein structures in stunning 3D using iCn3D</p>', unsafe_allow_html=True)

# ================= SEARCH SECTION =================
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.markdown("### 🔍 Enter PDB ID")
    pdb_id = st.text_input(
        "PDB ID",
        placeholder="e.g., 4HHB, 1ATP, 3J3Q",
        label_visibility="collapsed",
        key="pdb_input"
    ).upper()

    # Popular examples
    st.markdown("""
    <div style="text-align: center; margin-top: 1rem;">
        <small style="color: #64748b;">Popular examples:</small><br>
        <span class="feature-badge">4HHB (Hemoglobin)</span>
        <span class="feature-badge">1ATP (ATP Synthase)</span>
        <span class="feature-badge">3J3Q (CRISPR)</span>
        <span class="feature-badge">1CRN (Crambin)</span>
    </div>
    """, unsafe_allow_html=True)

# ================= VIEWER SECTION =================
if pdb_id:
    # Info panel
    st.markdown(f"""
    <div class="info-card">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
            <div>
                <h3 style="margin: 0; color: #1e293b;">Now Viewing: <span style="color: #667eea;">{pdb_id}</span></h3>
                <p style="margin: 0.5rem 0 0 0; color: #64748b;">Loading interactive 3D visualization...</p>
            </div>
            <a href="https://www.rcsb.org/structure/{pdb_id}" target="_blank" style="text-decoration: none;">
                <div style="background: #667eea; color: white; padding: 0.75rem 1.5rem; border-radius: 10px; font-weight: bold;">
                    📖 View Details on RCSB
                </div>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Controls explanation
    with st.expander("🎮 Viewer Controls & Features", expanded=False):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            **🖱️ Mouse Controls:**
            - **Left Click + Drag**: Rotate structure
            - **Right Click + Drag**: Pan/Move
            - **Scroll Wheel**: Zoom in/out
            - **Double Click**: Center on atom
            """)

        with col2:
            st.markdown("""
            **🎨 Display Options:**
            - Change color schemes
            - Toggle surface representation
            - Show/hide hydrogen bonds
            - Label atoms and residues
            """)

        with col3:
            st.markdown("""
            **🔬 Analysis Tools:**
            - Measure distances
            - View sequence alignment
            - Export images/videos
            - Save custom views
            """)

    # 3D Viewer
    icn3d_url = (
        "https://www.ncbi.nlm.nih.gov/Structure/icn3d/full.html"
        f"?pdbid={pdb_id}&bu=1&showanno=1&show2d=1&showsets=1"
    )

    components.html(
        f"""
        <style>
            body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
            }}
            iframe {{
                border: none;
                width: 100%;
                height: 100vh;
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            }}
        </style>
        <iframe
            src="{icn3d_url}"
            allow="fullscreen"
            loading="lazy"
        ></iframe>
        """,
        height=850,
        scrolling=False
    )

    # Additional info
    st.markdown("""
    <div style="background: #f1f5f9; padding: 1.5rem; border-radius: 15px; margin-top: 2rem;">
        <h4 style="margin: 0 0 1rem 0; color: #1e293b;">💡 Pro Tips</h4>
        <ul style="margin: 0; color: #475569;">
            <li>Use the toolbar at the top of the viewer for advanced visualization options</li>
            <li>Click on atoms to see detailed information about residues</li>
            <li>Use the "Color" menu to highlight different protein features</li>
            <li>Press 'H' key for help menu with keyboard shortcuts</li>
            <li>Save your custom views using the bookmark feature</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

else:
    # ================= EMPTY STATE =================
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #667eea11 0%, #764ba211 100%); border-radius: 20px; margin: 3rem 0;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">🔬</div>
        <h2 style="color: #475569; margin-bottom: 1rem;">Ready to Explore!</h2>
        <p style="color: #64748b; font-size: 1.1rem; max-width: 600px; margin: 0 auto 2rem auto;">
            Enter a PDB ID above to load and interact with a 3D protein structure.
            Rotate, zoom, and analyze molecular structures in real-time.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎮</div>
            <h3 style="color: #1e293b; margin-bottom: 0.5rem;">Interactive</h3>
            <p style="color: #64748b; margin: 0; font-size: 0.95rem;">
                Rotate, zoom, and explore structures with intuitive mouse controls
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Popular structures
    st.markdown("""
    <div class="popular-structures">
        <h4 style="color: #1e293b; margin-bottom: 1rem; text-align: center;">🔥 Try These Popular Structures:</h4>
        <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 0.75rem;">
            <span class="feature-badge">🩸 4HHB - Hemoglobin</span>
            <span class="feature-badge">⚡ 1ATP - ATP Synthase</span>
            <span class="feature-badge">✂️ 3J3Q - CRISPR-Cas9</span>
            <span class="feature-badge">🧬 1BNA - DNA Double Helix</span>
            <span class="feature-badge">💊 1CRN - Crambin</span>
            <span class="feature-badge">🦠 6VSB - SARS-CoV-2 Spike</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.9rem; padding: 1rem;">
    Powered by <a href="https://www.ncbi.nlm.nih.gov/Structure/icn3d/docs/icn3d.html" target="_blank" style="color: #667eea; text-decoration: none;">iCn3D Viewer</a> |
    Data from <a href="https://www.rcsb.org/" target="_blank" style="color: #667eea; text-decoration: none;">RCSB PDB</a> |
    Built with Streamlit 🎈
</div>
""", unsafe_allow_html=True)