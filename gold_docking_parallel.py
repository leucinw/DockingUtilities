
#===================================
#        Chengwen Liu              #
#      liuchw2010@gmail.com        #
#   University of Texas at Austin  #
#===================================

import os
import sys
import argparse
import subprocess
import concurrent.futures 
from datetime import datetime
  
def splitmol(mol,nfrag):
  fname, _ = os.path.splitext(mol)
  lines = open(mol).readlines()
  indices = []
  for i in range(len(lines)):
    if "MOLECULE" in lines[i]:
      indices.append(i)
  nlines = len(lines)
  indices.append(nlines-1)
  
  if len(indices) <= 5000:
    nfrag = 10
  nmolecule = int(len(indices)/nfrag) + 1
  for i in range(nfrag):
    istart = indices[i*nmolecule]
    if (i+1)*nmolecule < len(indices):
      iend = indices[(i+1)*nmolecule]
    else:
      iend = indices[-1]+1
    with open(f"{fname}_{i:03d}.mol2", "w") as f:
      for k in range(istart, iend):
        f.write(lines[k])
  return

def subone(mol):
  fname, _ = os.path.splitext(mol)
  dirname = os.path.join(homedir, fname)
  if not os.path.isdir(dirname):
    os.mkdir(dirname)
  os.chdir(dirname)
  os.system(f"ln -sf ../{mol}")
  os.system(f"ln -sf ../{protein}")
  with open("gold.conf", 'w') as f:
    for conf in confs:
      if "ligand_data_file" in conf:
        d = conf.split()
        f.write(f"{ligand_data_file} {mol} {npose}\n")
      else:
        f.write(conf)
  if not os.path.isfile("gold.log"):
    subprocess.run(goldcmd, shell=True)
  return

def submultiple(mols):  
  jobs = []
  with concurrent.futures.ProcessPoolExecutor() as executor:
    results = [executor.submit(subone, mol) for mol in mols]
    for f in concurrent.futures.as_completed(results):
      jobs.append(f.result())
  return 

def main():
  now = datetime.now().strftime("%b %d %Y %H:%M:%S")
  print(f"Program Starts at: {now}")
  parser = argparse.ArgumentParser()
  parser.add_argument('-ligands', dest = 'ligands',  nargs='+', help = "mol2 files", required=True)  
  parser.add_argument('-protein', dest = 'protein', help = "pdb file", required=True)  
  parser.add_argument('-nfrag', dest = 'nfrag', help = "number of fragments", type=int, default=100)  
  parser.add_argument('-npose', dest = 'npose', help = "number of poses", type=int, default=5)  
  args = vars(parser.parse_args())
  global ligands, protein, nfrag, npose
  ligands = args["ligands"]
  protein = args["protein"]
  nfrag = args["nfrag"]
  npose = args["npose"]

  global homedir, confs
  homedir = os.getcwd()
  
  rootdir = os.path.join(os.path.split(__file__)[0])
  #! prepare your gold.conf file carefully
  conffile = os.path.join(homedir, "gold.conf")
  if os.path.isfile(conffile):
    confs = open(conffile).readlines()
  else:
    sys.exit(f"Error: gold.conf is required to run GOLD\nYou can copy here: {rootdir}/gold.conf and ADAPT for your purpose!")
  
  global goldcmd
  #! adapt this command for your GOLD
  goldcmd = " /opt/CCDC/CCDC2020/Discovery_2020/bin/gold_auto gold.conf "
  
  for ligand in ligands:
    fname, _ = os.path.splitext(ligand)
    splitmol(ligand, nfrag)
  
  files = os.listdir()
  mols = []
  for f in files:
    for ligand in ligands:
      fname, _ = os.path.splitext(ligand)
      if (fname +"_" in f) and (f.endswith(".mol2")):
        mols.append(f)
  submultiple(mols)
  now = datetime.now().strftime("%b %d %Y %H:%M:%S")
  print(f"Program Finishes at: {now}")
  return

if __name__ == "__main__":
  main()