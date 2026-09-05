# 📦 `Solvent-Accessible-Area-Analyzer`

`sasa_viz` is a lightweight Python module designed for computational biology and chemistry workflows. It simplifies fetching Protein Data Bank (PDB) files, calculating Solvent Accessible Surface Area (SASA) via `freesasa`, mapping atomic area values onto Biopython structure objects, and rendering interactive 3D visualizations in JupyterLab using `py3Dmol`.

---

## 🛠️ Available Functions

1. `fetch_pdb` Downloads a `.pdb` structure file from the RCSB PDB database.
2. `load_structure` Parses a local PDB file into a Biopython `Structure` object.
3. `analyze_sasa` Calculates SASA values using `freesasa` and writes the calculated atomic SASA values directly into the **B-factor** fields of the Biopython structure atoms.
4. `render_sasa` Converts the analyzed structure into an interactive 3D canvas with a surface colored by SASA.

---

## 💻 Setup / Installation

```bash
# From the main directory
pip install -e .

# Try
python3 test_script.py
```

---

## 🚀 Usage Examples

### Example 1: Fetching & Analyzing an Online PDB Structure

```python
import sasa_viz as sv

# 1. Fetch PDB file from RCSB
filepath = sv.fetch_pdb("1CRN", output_dir="data")

# 2. Parse into a Biopython structure
structure = sv.load_structure(filepath, structure_id="1CRN")

# 3. Compute SASA and map to atomic B-factors
analyzed_struct, total_area = sv.analyze_sasa(structure, filepath)
print(f"Total SASA for 1CRN: {total_area:.2f} Å²")

# 4. Render 3D Surface in Jupyter
view = sv.render_sasa(analyzed_struct, opacity=0.85)
view.show()
```

---

### Example 2: Working with a Local PDB File

```python
import sasa_viz as sv

local_file = "data/2DAN.pdb"

# Load local PDB without making network calls
structure = sv.load_structure(local_file, structure_id="2DAN")

# Run analysis on local file
analyzed_struct, total_area = sv.analyze_sasa(structure, local_file)
print(f"Total SASA for 2DAN: {total_area:.2f} Å²")

# Render interactive model
view = sv.render_sasa(analyzed_struct, opacity=0.75, max_sasa=40.0)
view.show()
```

---
