import io
import freesasa
from Bio.PDB import PDBList, PDBParser, PDBIO
import py3Dmol

def fetch_pdb(pdb_code: str, output_dir: str = ".") -> str:
    """Fetches a PDB file from RCSB and returns the local file path."""
    pdbl = PDBList()
    filepath = pdbl.retrieve_pdb_file(pdb_code.upper(), pdir=output_dir, file_format="pdb")
    return filepath

def load_structure(filepath: str, structure_id: str = "structure"):
    """Parses a local PDB file path into a Biopython Structure object."""
    parser = PDBParser(QUIET=True)
    return parser.get_structure(structure_id, filepath)

def analyze_sasa(structure, filepath: str):
    """Calculates SASA from a structure file and maps the atomic SASA values

    directly into the structure's B-factor fields.
    """
    # 1. Parse with FreeSASA
    fs_structure = freesasa.Structure(filepath)
    result = freesasa.calc(fs_structure)

    # 2. Extract atomic SASA array from FreeSASA
    # FreeSASA stores calculated area for each atom sequentially
    n_atoms = fs_structure.nAtoms()

    # 3. Create a generator of all atoms in the Biopython structure
    # (Filtering out HETATMs/Water to match standard PDB atom counts if needed)
    bio_atoms = [atom for atom in structure.get_atoms()]

    # 4. Map SASA to B-factors safely using zip or bound-checked loop
    for i in range(min(n_atoms, len(bio_atoms))):
        try:
            sasa_val = result.atomArea(i)
            bio_atoms[i].set_bfactor(sasa_val)
        except (AssertionError, IndexError):
            bio_atoms[i].set_bfactor(0.0)

    return structure, result.totalArea()

def render_sasa(structure, opacity: float = 0.8, max_sasa: float = 30.0):
    """Converts a Biopython structure to a PDB string and renders in py3Dmol."""
    output_stream = io.StringIO()
    io_eng = PDBIO()
    io_eng.set_structure(structure)
    io_eng.save(output_stream)
    pdb_str = output_stream.getvalue()

    view = py3Dmol.view(width=800, height=500)
    view.addModel(pdb_str, "pdb")
    view.setStyle({"cartoon": {"color": "gray"}})
    view.addSurface(
        py3Dmol.VDW,
        {
            "opacity": opacity,
            "colorscheme": {"gradient": "rwb", "min": 0, "max": max_sasa, "prop": "b"},
        },
    )
    view.zoomTo()
    return view
