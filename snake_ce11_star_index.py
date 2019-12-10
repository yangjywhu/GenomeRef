import os
import pandas as pd

base_dir = "/data1/zhoulab/yangjiayi/reference/ce11"

os.chdir(base_dir)

rule all:
    input:
        "ce11_rRNA_index",

rule rRNA_index:
    input:
        fa = "ce11_anno_file/ce11_rRNA.fa",
        gtf = "ce11_anno_file/ce11_rRNA.gtf",
    output:
        index = directory("ce11_rRNA_index"),
    threads: 1
    shell:"""
        set +u; source ~/miniconda3/bin/activate seq; set -u
        mkdir -p {output.index}
        STAR --runThreadN {threads} \
            --runMode genomeGenerate \
            --genomeDir {output.index} \
            --genomeFastaFiles {input.fa} \
            --sjdbGTFfile {input.gtf} \
            --genomeSAindexNbases 6 \
            --outFileNamePrefix {output.index}/ \
            --sjdbOverhang 149
        set +u; conda deactivate; set -u
        """