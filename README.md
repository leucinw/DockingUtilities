# DockingUtilities
Collections of light programs for molecular docking simulations

## Programs 
* gold_docking_parallel.py: parallelly run GOLD docking using concurrent feature of Python module
* molecular_selector.py: select molecules according to molecular similarity. This is to reduce the number of molecules for further docking simulation
* pocket_finder.py: give a protein structure (in PDB) and one/more ligands (in mol2), find the binding pocket using GOLD docking
* print_docking_summary.py: various functions to print the summary of gold docking results

## Notes
* Only the GOLD docking is supported for now. Future development will involve other docking programs especially the free-of-charge ones.

