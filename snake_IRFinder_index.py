import os

rna1_mount = "/data1/zhoulab/yangjiayi/mu01_home"
base_dir = os.path.join(rna1_mount + "/reference/hg19")
ref_dir = os.path.join(rna1_mount + "/software/IRFinder-1.2.5/REF/extra-input-files")

os.chdir(base_dir)

# ruleorder: irf_index > run_irf

rule all:
    input:
        "hg19_IRFinder_v1.2.5_index"

rule irf_index_online:
    input:
        ercc_ref = os.path.join(ref_dir, "RNA.SpikeIn.ERCC.fasta.gz"),
        bed = os.path.join(ref_dir, "Human_hg19_wgEncodeDacMapabilityConsensusExcludable.bed.gz"),
        roi = os.path.join(ref_dir, "Human_hg19_nonPolyA_ROI.bed"),
    output:
        ref_dir = directory("hg19_IRFinder_v1.2.5_index"),
    threads: 5
    params:
        ftp_ref = "ftp://ftp.ensembl.org/pub/release-75/gtf/homo_sapiens/Homo_sapiens.GRCh37.75.gtf.gz"
    shell:"""
        set +u; source ~/miniconda3/bin/activate seq; set -u
        bin/IRFinder -m BuildRef -r {output.ref_dir} \
            -e {input.ercc_ref} -b {input.bed} -R {input.roi} \
            {params.ftp_ref}
        set +u; conda deactivate; set -u
        """
