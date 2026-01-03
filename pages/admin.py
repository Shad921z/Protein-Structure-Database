import streamlit as st
import sqlite3
import requests
import pandas as pd

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Admin Panel - Protein DB ",
    layout="wide",
    page_icon="🔐"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .admin-header {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(220, 38, 38, 0.3);
    }

    .login-container {
        max-width: 400px;
        margin: 4rem auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border: 2px solid #e2e8f0;
    }

    .section-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 2px solid #e2e8f0;
        margin-bottom: 2rem;
    }

    .section-title {
        color: #1e293b;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .stats-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #cbd5e1;
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #dc2626;
        margin-bottom: 0.5rem;
    }

    .stat-label {
        color: #64748b;
        font-size: 1rem;
    }

    .success-box {
        background: #dcfce7;
        border-left: 4px solid #16a34a;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }

    .error-box {
        background: #fee2e2;
        border-left: 4px solid #dc2626;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ================= PASSWORD GATE =================
ADMIN_PASSWORD = "admin123"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
    <div class="login-container">
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🔐</div>
            <h2 style="color: #1e293b; margin: 0;">Admin Access Required</h2>
            <p style="color: #64748b; margin-top: 0.5rem;">Enter password to continue</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    password = st.text_input("Password - pass: admin123", type="password", placeholder="Enter admin password")

    if st.button("🔓 Login", use_container_width=True, type="primary"):
        if password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.success("✅ Access granted!")
            st.rerun()
        else:
            st.error("❌ Incorrect password")

    st.stop()

# ================= DATABASE =================
DB_NAME = "protein_structure.db"
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

# ================= CREATE TABLES =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS protein (
    protein_id INTEGER PRIMARY KEY AUTOINCREMENT,
    protein_name TEXT,
    pdb_id TEXT UNIQUE,
    uniprot_id TEXT,
    organism TEXT,
    function TEXT,
    aa_length INTEGER,
    molecular_weight REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS protein_structure (
    structure_id INTEGER PRIMARY KEY AUTOINCREMENT,
    protein_id INTEGER,
    method TEXT,
    resolution REAL,
    ligand_present INTEGER,
    FOREIGN KEY (protein_id) REFERENCES protein(protein_id)
)
""")
conn.commit()

# ================= MOLECULAR WEIGHT =================
aa_weights = {
    'A': 89.1, 'R': 174.2, 'N': 132.1, 'D': 133.1,
    'C': 121.2, 'E': 147.1, 'Q': 146.1, 'G': 75.1,
    'H': 155.2, 'I': 131.2, 'L': 131.2, 'K': 146.2,
    'M': 149.2, 'F': 165.2, 'P': 115.1, 'S': 105.1,
    'T': 119.1, 'W': 204.2, 'Y': 181.2, 'V': 117.1
}

def calculate_molecular_weight(sequence):
    total = sum(aa_weights.get(aa, 0) for aa in sequence)
    return round(total / 1000, 2)

# ================= DATA FETCHING =================
def fetch_rcsb_data(pdb_id):
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()
    protein_name = data.get("struct", {}).get("title", "Unknown")
    method = data.get("exptl", [{}])[0].get("method") if data.get("exptl") else None
    resolution = data.get("rcsb_entry_info", {}).get("resolution_combined", [None])[0]
    ligands = data.get("rcsb_entry_container_identifiers", {}).get("nonpolymer_entity_ids", [])
    ligand_present = 1 if ligands else 0
    return protein_name, method, resolution, ligand_present, "Unknown"

def get_uniprot_and_organism(pdb_id):
    url = f"https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb_id}/1"
    r = requests.get(url)
    if r.status_code != 200:
        return None, "Unknown"
    data = r.json()
    uniprot_ids = data.get("rcsb_polymer_entity_container_identifiers", {}).get("uniprot_ids", [])
    uniprot_id = uniprot_ids[0] if uniprot_ids else None
    organism = "Unknown"
    src = data.get("rcsb_entity_source_organism", [])
    if src:
        organism = src[0].get("scientific_name", "Unknown")
    return uniprot_id, organism

def fetch_uniprot_data(uniprot_id):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    r = requests.get(url)
    if r.status_code != 200:
        return None, None
    data = r.json()
    sequence = data["sequence"]["value"]
    function = "No description available"
    for c in data.get("comments", []):
        if c.get("commentType") == "FUNCTION":
            texts = c.get("texts", [])
            if texts:
                function = texts[0].get("value", function)
    return sequence, function

def add_protein(pdb_id):
    rcsb = fetch_rcsb_data(pdb_id)
    if rcsb is None:
        return False, "RCSB data not found"
    protein_name, method, resolution, ligand_present, organism = rcsb
    uniprot_id, organism = get_uniprot_and_organism(pdb_id)
    if uniprot_id is None:
        return False, "UniProt mapping not found"
    sequence, function = fetch_uniprot_data(uniprot_id)
    if sequence is None:
        return False, "UniProt data not found"
    aa_length = len(sequence)
    molecular_weight = calculate_molecular_weight(sequence)
    cursor.execute("""
    INSERT OR IGNORE INTO protein
    (protein_name, pdb_id, uniprot_id, organism, function, aa_length, molecular_weight)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (protein_name, pdb_id, uniprot_id, organism, function, aa_length, molecular_weight))
    conn.commit()
    cursor.execute("SELECT protein_id FROM protein WHERE pdb_id = ?", (pdb_id,))
    row = cursor.fetchone()
    if row is None:
        return False, "Protein insert failed"
    protein_id = row[0]
    cursor.execute("SELECT structure_id FROM protein_structure WHERE protein_id = ?", (protein_id,))
    if cursor.fetchone():
        return True, "Protein already exists"
    cursor.execute("""
    INSERT INTO protein_structure (protein_id, method, resolution, ligand_present)
    VALUES (?, ?, ?, ?)
    """, (protein_id, method, resolution, ligand_present))
    conn.commit()
    return True, "Protein added successfully"

def delete_protein(pdb_id):
    try:
        cursor.execute("SELECT protein_id FROM protein WHERE pdb_id = ?", (pdb_id,))
        result = cursor.fetchone()
        if result is None:
            return False, f"Protein with PDB ID '{pdb_id}' not found"
        protein_id = result[0]
        cursor.execute("DELETE FROM protein_structure WHERE protein_id = ?", (protein_id,))
        cursor.execute("DELETE FROM protein WHERE protein_id = ?", (protein_id,))
        conn.commit()
        return True, f"Successfully deleted protein {pdb_id}"
    except Exception as e:
        conn.rollback()
        return False, f"Error: {str(e)}"

def get_protein_data(pdb_id):
    cursor.execute("""
    SELECT p.protein_id, p.protein_name, p.pdb_id, p.uniprot_id, p.organism, p.function,
           p.aa_length, p.molecular_weight, s.structure_id, s.method, s.resolution, s.ligand_present
    FROM protein p
    JOIN protein_structure s ON p.protein_id = s.protein_id
    WHERE p.pdb_id = ?
    """, (pdb_id,))
    return cursor.fetchone()

def update_protein(protein_id, structure_id, protein_name, organism, function,
                   aa_length, molecular_weight, method, resolution, ligand_present):
    try:
        cursor.execute("""
        UPDATE protein SET protein_name = ?, organism = ?, function = ?,
               aa_length = ?, molecular_weight = ? WHERE protein_id = ?
        """, (protein_name, organism, function, aa_length, molecular_weight, protein_id))
        cursor.execute("""
        UPDATE protein_structure SET method = ?, resolution = ?, ligand_present = ?
        WHERE structure_id = ?
        """, (method, resolution, ligand_present, structure_id))
        conn.commit()
        return True, "Protein updated successfully"
    except Exception as e:
        conn.rollback()
        return False, f"Error: {str(e)}"

# ================= HEADER =================
st.markdown("""
<div class="admin-header">
    <h1 style="margin: 0; font-size: 2.5rem;">🔐 Admin Panel</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
        Protein Structure Database Management
    </p>
</div>
""", unsafe_allow_html=True)

# ================= STATISTICS =================
cursor.execute("SELECT COUNT(*) FROM protein")
total_proteins = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM protein_structure WHERE ligand_present = 1")
proteins_with_ligands = cursor.fetchone()[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stat-number">{total_proteins}</div>
        <div class="stat-label">Total Proteins</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stat-number">{proteins_with_ligands}</div>
        <div class="stat-label">With Ligands</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stat-number">{total_proteins - proteins_with_ligands}</div>
        <div class="stat-label">Without Ligands</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ================= ADD PROTEIN =================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">➕ Add New Protein</div>', unsafe_allow_html=True)

pdb_input = st.text_input("Enter PDB ID", placeholder="e.g., 4HHB", key="add_input")

if st.button("🚀 Add Protein", use_container_width=True, type="primary"):
    if pdb_input:
        with st.spinner("Fetching data from RCSB and UniProt..."):
            success, message = add_protein(pdb_input.upper())
            if success:
                st.success(f"✅ {message}")
                st.rerun()
            else:
                st.error(f"❌ {message}")
    else:
        st.warning("⚠️ Please enter a PDB ID")

st.markdown('</div>', unsafe_allow_html=True)

# ================= DELETE PROTEIN =================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🗑️ Delete Protein</div>', unsafe_allow_html=True)

pdb_delete_input = st.text_input("Enter PDB ID to delete", placeholder="e.g., 4HHB", key="delete_input")

if st.button("🔥 Delete Protein", use_container_width=True, type="secondary"):
    if pdb_delete_input:
        success, message = delete_protein(pdb_delete_input.upper())
        if success:
            st.success(f"✅ {message}")
            st.rerun()
        else:
            st.error(f"❌ {message}")
    else:
        st.warning("⚠️ Please enter a PDB ID")

st.markdown('</div>', unsafe_allow_html=True)

# ================= UPDATE PROTEIN =================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">✏️ Update Protein Information</div>', unsafe_allow_html=True)

pdb_update_input = st.text_input("Enter PDB ID to update", placeholder="e.g., 4HHB", key="update_search")

if st.button("🔍 Search Protein", key="search_btn"):
    if pdb_update_input:
        data = get_protein_data(pdb_update_input.upper())
        if data:
            st.session_state.protein_data = data
            st.success(f"✅ Found: {data[1]}")
        else:
            st.error("❌ Protein not found")
    else:
        st.warning("⚠️ Please enter a PDB ID")

if "protein_data" in st.session_state:
    data = st.session_state.protein_data

    st.markdown("**📝 Current Data - Edit Below:**")

    with st.form("update_form"):
        protein_name = st.text_input("Protein Name", value=data[1])
        organism = st.text_input("Organism", value=data[4])
        function = st.text_area("Function", value=data[5], height=100)

        col1, col2 = st.columns(2)
        with col1:
            aa_length = st.number_input("AA Length", value=data[6], min_value=0)
            molecular_weight = st.number_input("Molecular Weight (kDa)", value=float(data[7]), min_value=0.0)
        with col2:
            method = st.text_input("Method", value=data[9] or "")
            resolution = st.number_input("Resolution (Å)", value=float(data[10]) if data[10] else 0.0, min_value=0.0)

        ligand_present = st.selectbox("Ligand Present", options=[0, 1], index=data[11],
                                     format_func=lambda x: "Yes" if x == 1 else "No")

        submitted = st.form_submit_button("💾 Update Protein", use_container_width=True, type="primary")

        if submitted:
            success, message = update_protein(data[0], data[8], protein_name, organism, function,
                                            aa_length, molecular_weight, method, resolution, ligand_present)
            if success:
                st.success(f"✅ {message}")
                del st.session_state.protein_data
                st.rerun()
            else:
                st.error(f"❌ {message}")

st.markdown('</div>', unsafe_allow_html=True)

# ================= STORED PROTEINS TABLE =================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Stored Proteins Database</div>', unsafe_allow_html=True)

query = """
SELECT p.protein_name, p.pdb_id, p.uniprot_id, p.organism, p.aa_length,
       p.molecular_weight, s.method, s.resolution, s.ligand_present
FROM protein p
JOIN protein_structure s ON p.protein_id = s.protein_id
"""

df = pd.read_sql_query(query, conn)

if not df.empty:
    st.dataframe(df, use_container_width=True, height=400)
else:
    st.info("📭 No proteins in database yet. Add some above!")

st.markdown('</div>', unsafe_allow_html=True)

# ================= LOGOUT =================
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚪 Logout", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()