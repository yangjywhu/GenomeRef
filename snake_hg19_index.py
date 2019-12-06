import os

base_dir = "/data1/zhoulab/yangjiayi/reference/hg19"
anno_dir = "/data1/zhoulab/yangjiayi/reference/hg19/hg19_anno_file"

os.chdir(base_dir)

rule all:
    input:
        "hg19_star_index",

rule hg19_star_index:
    input:
        gtf = "hg19_anno_file/hg19_GRCh37_gencode_20190821.gtf",
        fa = "hg19_anno_file/hg19_GRCh37_gencode_20190905.fa",
    output:
        index_dir = directory("hg19_star_index"),
    threads: 14
    shell:"""
        set +u; source ~/miniconda3/bin/activate seq; set -u
        mkdir -p {output.index_dir}
        STAR --runThreadN {threads} \
            --runMode genomeGenerate \
            --genomeDir {output.index_dir} \
            --genomeFastaFiles {input.fa} \
            --sjdbGTFfile {input.gtf} \
            --sjdbOverhang 100 \
            --genomeSAindexNbases 12 
        set +u; conda deactivate; set -u
        """