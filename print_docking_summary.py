
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

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('choice', type=str.lower, choices=['bestgrid', 'bestligand'])
  args = parser.parse_args()
  actions = {'bestgrid':bestgrid, 'bestligand':bestligand}
  print(actions[args.choice])
  actions[args.choice]()
  return

if __name__ == "__main__":
  main()