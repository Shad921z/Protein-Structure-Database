import streamlit as st
import sqlite3
import requests
import pandas as pd

# ================= PASSWORD GATE =================

ADMIN_PASSWORD = "admin123"  # change this

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Admin Access Required")

    password = st.text_input("Enter admin password", type="password")

    if st.button("Login"):
        if password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.success("Access granted")
            st.rerun()
        else:
            st.error("Incorrect password")

    st.stop()

# ================= DATABASE =================

DB_NAME = "protein_structure.db"
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

# ================= CREATE TABLES (SAFE) =================

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
    total = 0
    for aa in sequence:
        if aa in aa_weights:
            total += aa_weights[aa]
    return round(total / 1000, 2)

# ================= DATA FETCHING =================

def fetch_rcsb_data(pdb_id):
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    r = requests.get(url)

    if r.status_code != 200:
        return None

    data = r.json()

    protein_name = data.get("struct", {}).get("title", "Unknown")

    method = None
    if data.get("exptl"):
        method = data["exptl"][0].get("method")

    resolution = None
    info = data.get("rcsb_entry_info", {})
    if info.get("resolution_combined"):
        resolution = info["resolution_combined"][0]

    # ✅ CORRECT ligand detection ------ not working
    container_ids = data.get("rcsb_entry_container_identifiers", {})
    ligands = container_ids.get("nonpolymer_entity_ids", [])
    ligand_present = 1 if len(ligands) > 0 else 0

    return protein_name, method, resolution, ligand_present, "Unknown"


def get_uniprot_and_organism(pdb_id):
    url = f"https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb_id}/1"
    r = requests.get(url)

    if r.status_code != 200:
        return None, "Unknown"

    data = r.json()

    # UniProt ID
    ids = data.get("rcsb_polymer_entity_container_identifiers", {})
    uniprot_ids = ids.get("uniprot_ids", [])
    uniprot_id = uniprot_ids[0] if uniprot_ids else None

    # Organism
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

# ================= INGESTION =================

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
    INSERT INTO protein_structure
    (protein_id, method, resolution, ligand_present)
    VALUES (?, ?, ?, ?)
    """, (protein_id, method, resolution, ligand_present))
    conn.commit()

    return True, "Protein added successfully"

# ================= UI =================

st.title("🧬 Protein Structure Database (Admin)")

st.subheader("➕ Add Protein by PDB ID")

pdb_input = st.text_input("Enter PDB ID (e.g. 4HHB)").upper()

if st.button("Add Protein"):
    if pdb_input:
        success, message = add_protein(pdb_input)
        if success:
            st.success(message)
        else:
            st.error(message)
    else:
        st.warning("Please enter a PDB ID")

st.divider()

st.subheader("📊 Stored Proteins")

query = """
SELECT
    p.protein_name,
    p.pdb_id,
    p.uniprot_id,
    p.organism,
    p.aa_length,
    p.molecular_weight,
    s.method,
    s.resolution,
    s.ligand_present
FROM protein p
JOIN protein_structure s ON p.protein_id = s.protein_id
"""

df = pd.read_sql_query(query, conn)

st.dataframe(df, use_container_width=True)


