import argparse as ag
import sys
import os

# ap = ag.ArgumentParser(prog=os.path.basename(sys.argv[0]), usage=__doc__)
# ap.add_argument('-i', required=True, help='input mapping directory, result will be output in STDOUT')
# ap.add_argument('-o', required=True, help='output gtf file')
# args = ap.parse_args()

# input_pas = args.i
# out_gtf =  args.o

input_pas = r"D:\MyDoc\OneDrive\Doc\Lab\analysis\hl\pas_anno\human.PAS.txt"
out_gtf = r"D:\MyDoc\OneDrive\Doc\Lab\analysis\hl\pas_anno\hg19_PAS.gtf"

def print_record(pas, file_handle):
    # print one line of gtf file
    attri = 'gene_id "%s";' % pas[6]
    start = int(pas[2]) - 9 
    end = int(pas[2]) + 10 
    record = [pas[1], "polyA_DB", "PAS", start, end, 
              '.', pas[3], '.', attri]
    print(*record, sep='\t', file=file_handle)

# output 3' most exon and gene with id
with open(input_pas, 'r') as fi, \
  open(out_gtf, 'w') as fo:
    head = fi.readline()
    for line in fi:        
        line_list = line.strip().split('\t')
        # select 3' most exon
        if line_list[5] != "3' most exon":
            continue
        # del gene without id
        if line_list[6] == 'na':
            continue
        print_record(line_list, fo)