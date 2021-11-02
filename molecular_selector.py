
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

def select_similar(tempmol):
  selected = []
  for target in targets:
    f1,_ = os.path.splitext(tempmol)
    f2,_ = os.path.splitext(target)
    fname = f1 + "_" + f2
    cmdstr = f"babel {tempmol} {target} -ofpt >{fname}.out 2>err; wait"
    if not os.path.isfile(f"{fname}.out"):
      os.system(cmdstr)
    else:
      print(f"{fname}.out exist!")
    for line in open(f"{fname}.out").readlines():
      if "Tanimoto " in line:
        d = line.split()
        molname = d[0][1:]
        similarity = float(d[-1])
        if similarity >= score:
          selected.append([f2, molname, similarity])
  return selected

def write_mols(file_mols):
  for fname in file_mols: 
    mols = file_mols[fname]
    with open(fname + ".mol2.sel", "w") as fw:
      with open(fname + ".mol2", "r") as fr:
        iRead = False
        for line in fr:
          if "MOLECULE" in line:
            iRead = False
          if line[:-1] in mols:
            iRead = True
            fw.write("@<TRIPOS>MOLECULE\n")
          if iRead:
            fw.write(line)
  return
  
def write_selected():
  ts = []
  for t in targets:
    f, _ = os.path.splitext(t)
    ts.append(f)
  vs = [[] for i in range(len(ts))]
  target_selected = dict(zip(ts,vs)) 
  jobs = []
  with concurrent.futures.ProcessPoolExecutor() as executor:
    results = [executor.submit(select_similar, temp) for temp in templates]
    for f in concurrent.futures.as_completed(results):
      jobs.append(f.result())
  for job in jobs:
    for j in job:
      [filename, molname, _] = j
      if molname not in target_selected[filename]:
        target_selected[filename] += [molname]
  print("\nMOLECULES SELECTION COMPLETED !!\nWriting the selected molecules into one file...")
  jobs = []
  with concurrent.futures.ProcessPoolExecutor() as executor:
    results = [executor.submit(write_mols, {ff:target_selected[ff]}) for ff in target_selected]
    for xx in concurrent.futures.as_completed(results):
      jobs.append(xx.result())

  selectedmol = f"selected_{str(score)}.mol2"
  catcmd = f"cat *.mol2.sel > {selectedmol}"
  os.system(catcmd)
  os.system("rm -rf *.mol2.sel")
  return

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-temp', dest = 'templates',  nargs='+', help = "template mol2 files", required=True)  
  parser.add_argument('-tar', dest = 'targets',  nargs='+', help = "target mol2 files", required=True)  
  parser.add_argument('-score', dest = 'score', help = "Tanimoto index lower limit", type=float, required=True)  
  args = vars(parser.parse_args())
  global templates, targets, score 
  templates = args["templates"]
  targets = args["targets"]
  score = args["score"]
  write_selected()
  return

if __name__ == "__main__":
  main()
