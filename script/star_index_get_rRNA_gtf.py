import argparse as ag
import sys
import os

ap = ag.ArgumentParser(prog=os.path.basename(sys.argv[0]), usage=__doc__)
ap.add_argument('-i', required=True, help='input genome gtf file')
ap.add_argument('-o', required=True, help='output rRNA gtf file')
args = ap.parse_args()

genome_gtf = args.i
out_gtf = args.o

# genome_gtf = r"C:\analysis\hg19_GRCh37.gtf"
# out_gtf = r"C:\analysis\hg19_rRNA.gtf"

with open(genome_gtf, 'r') as fi, \
  open(out_gtf, 'w') as fo:
    for line in fi:
        if "rRNA" in line:
            line_list = line.strip().split('\t')
            if line_list[2] == "gene":
                if "chr" in line_list[0]: 
                    if line_list[0] not in ["chrX", "chrY", "chrM"]:
                        fo.write(line)