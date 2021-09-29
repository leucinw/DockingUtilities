# DockingUtilities
Collections of light programs for molecular docking simulations

## Programs 
* `gold_docking_parallel.py`: parallelly run GOLD docking using concurrent feature of Python module. For example, if the computer have 64 threads, then there will be 64 docking jobs running at the same time.
* `molecular_selector.py`: select molecules according to molecular similarity with [Tanimoto index](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-015-0069-3). This is to reduce the number of molecules for further docking simulation. For example, after 1 Million ligands being screened, select top 50 as the `template` and search for `similar` molecules in the remaining database. Then docking on the selected molecules can be performed using `gold_docking_parallel.py` described above. This approach has been proven effective.
* `pocket_finder.py`: give a protein structure (in PDB) and one/more ligands (in mol2), find the binding pocket using GOLD docking. The idea is to do a brute-force scan of the predefined grid points around/in the protein.
* `print_docking_summary.py`: print the docking results either with `bestgrid` or `bestligand` function.

## Future developments
* Only the GOLD docking is supported for now. Future development will involve other docking programs especially the free-of-charge ones.
* Protein and ligand files used for docking are vital in molecular docking. Utilities such as `gold_utils`, `openbabel`, pka prediction tools etc will be wrapped for preparing the files.

