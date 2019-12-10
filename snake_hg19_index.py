import os

base_dir = "/data1/zhoulab/yangjiayi/reference/hg19"
anno_dir = "/data1/zhoulab/yangjiayi/reference/hg19/hg19_anno_file"
script_dir = "/data1/zhoulab/yangjiayi/reference/github/GenomeRef/script"

os.chdir(base_dir)

rule all:
    input:
        "hg19_star_index",
        "hg19_rRNA_star_index",

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

rule hg19_rRNA_star_index:
    input:
        geno_gtf = "hg19_anno_file/hg19_GRCh37_gencode_20190821.gtf",
        geno_fa = "hg19_anno_file/hg19_GRCh37_gencode_20190905.fa",
    output:
        rRNA_gtf = "hg19_anno_file/hg19_rRNA.gtf",
        rRNA_fa = "hg19_anno_file/hg19_rRNA.fa",
        index_dir = directory("hg19_rRNA_star_index"),
    threads: 14
    shell:"""
        set +u; source ~/miniconda3/bin/activate seq; set -u
        python {script_dir}/star_index_get_rRNA_gtf.py \
            -i {input.geno_gtf} -o {output.rRNA_gtf}
        bedtools getfasta -fi {input.geno_fa} -fo {output.rRNA_fa} \
            -bed {output.rRNA_gtf} -name+
        mkdir -p {output.index_dir}
        STAR --runThreadN {threads} \
            --runMode genomeGenerate \
            --genomeDir {output.index_dir} \
            --genomeFastaFiles {output.rRNA_fa} \
            --genomeSAindexNbases 7 
        set +u; conda deactivate; set -u
        """