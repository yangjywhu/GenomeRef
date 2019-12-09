import argparse as ag
import sys
import os

# ap = ag.ArgumentParser(prog=os.path.basename(sys.argv[0]), usage=__doc__)
# ap.add_argument('-i', required=True, help='input mapping directory, result will be output in STDOUT')
# ap.add_argument('-o', required=True, help='output gtf file prefix, files will names as "xxx_pPAS.gtf" and "xxx_dPAS.gtf"')
# args = ap.parse_args()

# input_pas = args.i
# out_pfx =  args.o

input_pas = r"D:\MyDoc\OneDrive\Doc\Lab\analysis\hl\pas_anno\human.PAS.txt"
out_pfx = r"D:\MyDoc\OneDrive\Doc\Lab\analysis\hl\pas_anno\hg19_"

# get PAS with "3' most exon" only
temp_file = input_pas + ".temp"

def print_record(pas, file_handle, distance):
    # print one line of gtf file
    attri = 'gene_id "%s";' % pas[6]
    start = int(pas[2]) - 9 
    end = int(pas[2]) + 10 
    record = [pas[1], "polyA_DB", distance, start, end, 
              '.', pas[3], '.', attri]
    print(*record, sep='\t', file=file_handle)

def plus_or_minus(queue, f1, f2, d1, d2):
    # get pPAS (diff with last) and dPAS (diff with next)
    if queue[0][6] != queue[1][6]:
        print_record(queue[1], f1, d1)
    if queue[1][6] != queue[2][6]:
        print_record(queue[1], f2, d2)

# create a queue, to store treated line, last line and next line
queue = [[None] * 18] *3

# output 3' most exon and gene with id
with open(input_pas, 'r') as fi, \
  open(temp_file, 'w') as fo:
    head = fi.readline()
    for line in fi:        
        line_list = line.strip().split('\t')
        # select 3' most exon
        if line_list[5] != "3' most exon":
            continue
        # del gene without id
        if line_list[6] == 'na':
            continue
        fo.write(line)
    # print a end line, to make queue work normally
    print(*([None] * 18), sep='\t', file=fo)

with open(temp_file, 'r') as fi, \
  open(out_pfx + "pPAS.gtf", 'w') as fp, \
  open(out_pfx + "dPAS.gtf", 'w') as fd:
    for line in fi:
        # read line and split as a list
        line_list = line.strip().split('\t')
        # queue in & queue out
        queue.pop(0)
        queue.append(line_list)
        # remove gene with a single PAS
        if queue[1][1] == None:
            continue
        if queue[0][6] != queue[1][6] and queue[1][6] != queue[2][6]:
            continue
        if queue[1][3] == '+':
            plus_or_minus(queue, fp, fd, "pPAS", "dPAS")
        else:
            plus_or_minus(queue, fd, fp, "dPAS", "pPAS")
            