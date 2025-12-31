#  Protein Structure Database

An interactive web-based application to explore **protein 3D structures** and **ligand molecular structures** using publicly available biological databases.

The project is designed for **students and beginners in bioinformatics** to understand protein structures without dealing with complex file formats.

---

##  Features

-  Search proteins using **PDB ID**
-  Interactive **3D protein structure visualization** (Mol* / iCn3D)
-  Display **ligand molecular structures** using PubChem (CID-based)
-  Structured **SQLite protein database**
-  **Admin-only access** for data ingestion
-  Clean **multi-page Streamlit interface**

---

##  Data Sources

- **RCSB Protein Data Bank (PDB)** – protein structure metadata
- **NCBI iCn3D / Mol\*** – 3D structure visualization
- **PubChem** – ligand molecular structures (2D/3D)

---

##  Tech Stack

- **Python**
- **Streamlit** (frontend & UI)
- **SQLite** (database)
- **REST APIs** (RCSB, PubChem)
- **HTML iFrames** (3D visualization)

---

##  Project Structure

protein_structuredb/
│  
├── home.py # Home page  
├── protein_structure.db # SQLite database  
├── requirements.txt  
├── pages/  
│ ├── 1_Admin.py # Admin panel (add proteins)  
│ ├── 2_3D_Structure.py # 3D structure viewer  
│ ├── 3_Search.py # Protein search & detail view  
  

---

##  How to Run the Project

### 1️ Clone the repository
```bash
git clone https://github.com/shad921z/protein-structure-database.git
cd protein-structure-database 
```

### 2️ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️ Run the application

```bash
streamlit run app.py
```

##  Admin Access

The admin panel is protected using a session-based password gate.
Only the admin can add new protein data to the database.

##  Intended Audience

- Life science students
- Beginners in bioinformatics
- Educators demonstrating protein structures
- Developers exploring biology-related applications

##  Future Improvements

- Automatic ligand detection from PDB entries
- Protein–ligand interaction visualization
- Advanced filtering (organism, method, resolution)
- Deployment on Streamlit Cloud
- User authentication (viewer vs admin roles)



