import streamlit as st

st.set_page_config(layout="wide")

st.title("🧬 3D Structure Viewer")
st.subheader("ENETR PDB ID BELOW")
pdb_id = st.text_input(" ").upper()

if pdb_id:
    icn3d_url = (
        "https://www.ncbi.nlm.nih.gov/Structure/icn3d/full.html"
        f"?pdbid={pdb_id}&bu=1&showanno=1&source=full-feature"
    )

    st.components.v1.html(
        f"""
        <iframe
            src="{icn3d_url}"
            style="
                width:100vw;
                height:92vh;
                border:none;
                background:black;
            ">
        </iframe>
        """,
        height=900
    )


