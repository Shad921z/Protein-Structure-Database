import streamlit as st

st.set_page_config(
    page_title="Protein Structure Database",
    layout="wide",
    page_icon="🧬",
    initial_sidebar_state="collapsed"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    .hero-subtitle {
        font-size: 1.5rem;
        opacity: 0.95;
        margin-bottom: 1rem;
    }

    .hero-description {
        font-size: 1.1rem;
        opacity: 0.9;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* Feature cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
        border: 2px solid #e2e8f0;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }

    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .feature-title {
        color: #1e293b;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }

    .feature-text {
        color: #64748b;
        font-size: 1rem;
        line-height: 1.6;
    }

    /* Target audience section */
    .audience-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }

    /* Navigation buttons */
    .nav-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 2px solid #e2e8f0;
        height: 100%;
    }

    .nav-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }

    .nav-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }

    /* Footer */
    .custom-footer {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 3rem 2rem 2rem 2rem;
        border-radius: 20px;
        margin-top: 4rem;
        color: white;
    }

    .footer-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }

    .social-links {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }

    .social-link {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.1);
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        text-decoration: none;
        color: white;
        transition: all 0.3s ease;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }

    .social-link:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.4);
    }

    .footer-bottom {
        text-align: center;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        margin-top: 2rem;
        color: rgba(255, 255, 255, 0.7);
    }

    /* Section headers */
    .section-header {
        font-size: 2rem;
        font-weight: 600;
        color: #1e293b;
        margin: 3rem 0 1.5rem 0;
        text-align: center;
    }

    .section-divider {
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        margin: 0 auto 2rem auto;
        border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ================= HERO SECTION =================
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🧬 Protein Structure Database</div>
    <div class="hero-subtitle">Explore the World of Proteins in 3D</div>
    <div class="hero-description">
        An interactive platform to store, search, and visualize protein structures using
        publicly available biological databases such as RCSB PDB, NCBI, and PubChem.
        Designed for students, educators, and bioinformatics enthusiasts.
    </div>
</div>
""", unsafe_allow_html=True)

# ================= KEY FEATURES =================
st.markdown('<div class="section-header">✨ Key Features</div>', unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
<<<<<<< HEAD
    if st.button("🔍 Search Protein"):
        st.switch_page("pages/1_Search.py")
=======
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Smart Search</div>
        <div class="feature-text">
            Search proteins using PDB IDs or protein names with instant results from our curated database.
        </div>
    </div>
    """, unsafe_allow_html=True)
>>>>>>> 30ae89b (commit)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🧬</div>
        <div class="feature-title">3D Visualization</div>
        <div class="feature-text">
            Interactive 3D protein structure viewer powered by iCn3D with full rotation and zoom controls.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💊</div>
        <div class="feature-title">Ligand Analysis</div>
        <div class="feature-text">
            View and analyze bound ligand molecules with detailed structural information.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔐</div>
        <div class="feature-title">Admin Control</div>
        <div class="feature-text">
            Secure admin panel for adding, updating, and managing protein entries in the database.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Structured Data</div>
        <div class="feature-text">
            Well-organized protein database with key metrics like molecular weight, resolution, and more.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Fast & Reliable</div>
        <div class="feature-text">
            Lightning-fast queries with reliable data from RCSB PDB and UniProt databases.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================= WHO IS THIS FOR =================
st.markdown('<div class="section-header">👩‍🔬 Who Is This For?</div>', unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="audience-card">
        <h4 style="margin: 0 0 0.5rem 0; color: #1e293b;">🎓 Students</h4>
        <p style="margin: 0; color: #475569;">
            Perfect for life science students learning structural biology and bioinformatics concepts.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="audience-card">
        <h4 style="margin: 0 0 0.5rem 0; color: #1e293b;">👨‍🏫 Educators</h4>
        <p style="margin: 0; color: #475569;">
            Ideal for demonstrating protein structures in classrooms and creating engaging lessons.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="audience-card">
        <h4 style="margin: 0 0 0.5rem 0; color: #1e293b;">🔬 Researchers</h4>
        <p style="margin: 0; color: #475569;">
            Useful for quick protein structure lookups and preliminary structural analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="audience-card">
        <h4 style="margin: 0 0 0.5rem 0; color: #1e293b;">💻 Developers</h4>
        <p style="margin: 0; color: #475569;">
            Great reference for building biology-focused applications and learning bioinformatics APIs.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ================= NAVIGATION =================
st.markdown('<div class="section-header">🚀 Get Started</div>', unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="nav-card">
        <div class="nav-icon">🔍</div>
        <h3 style="color: #1e293b; margin-bottom: 0.5rem;">Search Protein</h3>
        <p style="color: #64748b; margin-bottom: 1.5rem;">
            Find and explore protein structures by PDB ID or name
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch Search", key="search_btn", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Search.py")

with col2:
    st.markdown("""
    <div class="nav-card">
        <div class="nav-icon">🧬</div>
        <h3 style="color: #1e293b; margin-bottom: 0.5rem;">3D Viewer</h3>
        <p style="color: #64748b; margin-bottom: 1.5rem;">
            Visualize protein structures in interactive 3D space
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch Viewer", key="viewer_btn", use_container_width=True, type="primary"):
        st.switch_page("pages/2_3D_Structure.py")

with col3:
<<<<<<< HEAD
    if st.button("🔐 Admin Panel"):
        st.switch_page("pages/Admin.py")

st.divider()

# ================= FOOTER =================

st.caption(
    "📌 Data sources: RCSB PDB, NCBI iCn3D, PubChem | Built using Python & Streamlit"
)
=======
    st.markdown("""
    <div class="nav-card">
        <div class="nav-icon">🔐</div>
        <h3 style="color: #1e293b; margin-bottom: 0.5rem;">Admin Panel</h3>
        <p style="color: #64748b; margin-bottom: 1.5rem;">
            Manage database entries and protein data
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch Admin", key="admin_btn", use_container_width=True, type="primary"):
        st.switch_page("pages/admin.py")
>>>>>>> 30ae89b (commit)
