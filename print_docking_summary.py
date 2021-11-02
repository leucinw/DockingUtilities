
#===================================
#        Chengwen Liu              #
#      liuchw2010@gmail.com        #
#   University of Texas at Austin  #
#===================================

import os
import argparse

def bestligand():
  files = os.listdir()
  records = []
  scores = []
  grepstr = "grep mol2 */bestranking.lst --no-filename > tmp.txt"
  os.system(grepstr)
  with open("tmp.txt") as fr:
    for line in fr:
      records.append(line)
      scores.append(float(line.split()[0]))
  records = [x for _,x in sorted(zip(scores,records), reverse=True)]
  t1 = "#     Score     S(PLP)   S(hbond)     S(cho)   S(metal)  DE(clash)   "
  t2 = "DE(tors)     intcor     time                               File name"
  t3 = "                Ligand name\n"
  with open("bestranking.lst", "w") as fw:
    fw.write(t1 + t2 + t3)
    for r in records:
      fw.write(r)
  return

def bestgrid():
  files = os.listdir()
  records = []
  scores = []
  ligands = []
  for f in files:
    if ('grid_' in f) and os.path.isdir(f):
      result = os.path.join(f, "bestranking.lst")
      if os.path.isfile(result):
        with open(result) as fr:
          for line in fr:
            if "mol2" in line:
              records.append(' ' + f + "   " + line)
              scores.append(float(line.split()[0]))
              ligand = line.split()[-1][1:-1]
              if ligand not in ligands:
                ligands.append(ligand)
  records = [x for _,x in sorted(zip(scores,records), reverse=True)]
  t0 = "#%16s   "%"GRID"
  t1 = "     Score     S(PLP)   S(hbond)     S(cho)   S(metal)  DE(clash)   "
  t2 = "DE(tors)     intcor     time                               File name"
  t3 = "                Ligand name\n"
  with open("bestranking.lst", "w") as fw:
    fw.write(t0 + t1 + t2 + t3)
    for r in records:
      fw.write(r)
  if len(ligands) > 1:
    for ligand in ligands:
      fname = f"bestranking_{ligand}.lst"
      with open(fname, 'w') as fw:
        fw.write(t0 + t1 + t2 + t3)
    for ligand in ligands:
      fname = f"bestranking_{ligand}.lst"
      grepstr = f"grep {ligand} bestranking.lst >> {fname}"
      os.system(grepstr)
  return

def topscore():
  currdir = os.getcwd().split("/")[-1]
  if not os.path.isfile("bestranking.lst"):
    sys.exit("bestranking.lst does not exist")
  i = 0
  topmols = []
  with open("bestranking.lst", 'r') as f:
    while True:
      line = f.readline()
      if "mol2" in line:
        topmols.append(line.split()[-2].split("./")[-1][:-1])
        i += 1
      if i == ntop:break
  os.system(f"mkdir -p {currdir}_top{ntop}")
  os.system(f"cp bestranking.lst ./{currdir}_top{ntop}")
  for mol in topmols:
    os.system(f"cp */{mol} ./{currdir}_top{ntop}")
  return

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('choice', type=str.lower, choices=['bestgrid', 'bestligand', 'topscore'])
  parser.add_argument('-ntop', dest = 'ntop', type=int, default=10)
  args = vars(parser.parse_args())
  global ntop
  ntop = args['ntop']
  actions = {'bestgrid':bestgrid, 'bestligand':bestligand, 'topscore':topscore}
  actions[args["choice"]]()
  return

if __name__ == "__main__":
  main()