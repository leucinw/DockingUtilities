
#===================================
#        Chengwen Liu              #
#      liuchw2010@gmail.com        #
#   University of Texas at Austin  #
#===================================

import os

def main():
  files = os.listdir()
  records = []
  scores = []
  for f in files:
    if os.path.isdir(f):
      result = os.path.join(f, "bestranking.lst")
      if os.path.isfile(result):
        with open(result) as fr:
          for line in fr:
            if "mol2" in line:
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

if __name__ == "__main__":
  main()