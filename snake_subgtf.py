import os

base_dir = "/data1/zhoulab/yangjiayi/reference/hg19"
anno_dir = "/data1/zhoulab/yangjiayi/reference/hg19/hg19_anno_file"

gene_types = ["protein_coding", "lincRNA"]

os.chdir(base_dir)

rule all:
    input:
        expand("hg19_anno_file/gene_type_gtf/hg19_{gene_type}.gtf",
               gene_type=gene_types),

rule split_gtf:
    input:
        gtf = "hg19_anno_file/hg19_GRCh37_gencode_20190821.gtf",
    output: 
        gtf = "hg19_anno_file/gene_type_gtf/hg19_{gene_type}.gtf",
        log = "hg19_anno_file/gene_type_gtf/{gene_type}_record_num.log",
    run:
        shell("mkdir -p hg19_anno_file/gene_type_gtf")
        total_num, sub_num = 0, 0
        with open(input.gtf, 'r') as fi, \
          open(output.gtf, 'w') as fo:
            for line in fi:
                total_num += 1
                if wildcards.gene_type in line:
                    fo.write(line)
                    sub_num += 1
        with open(output.log, 'w') as f:
            print("all record :", total_num - 5, file=f)
            print(wildcards.gene_type, ":", sub_num, file=f)