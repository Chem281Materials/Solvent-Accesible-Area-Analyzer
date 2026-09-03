import sasa_viz as sv

# 1. Fetch PDB file from RCSB
filepath = sv.fetch_pdb("1CRN", output_dir="data")

# 2. Parse into a Biopython structure
structure = sv.load_structure(filepath, structure_id="1CRN")

# 3. Compute SASA and map to atomic B-factors
analyzed_struct, total_area = sv.analyze_sasa(structure, filepath)
print(f"Total SASA for 1CRN: {total_area:.2f} Å²")
