import os

data1_dir = "/data1/zhoulab/yangjiayi"
base_dir = data1_dir + "/project/mettle3KD_RNAseq"
anno_dir = data1_dir + "/references/hg19/hg19_anno_file"
soft_dir = data1_dir + "/softwares/IRFinder"
samples = ["NM-NC", "NE-NC", "CE-NC"]
treat_groups = ["NE-NC", "CE-NC"]

os.chdir(base_dir)

# ruleorder: irf_index > run_irf

rule all:
    input:
        #"result/IRFiner_finish.txt",
        expand("result/irfinder/{sample}", sample=samples),
        #expand("result/irfinder/{treat_group}_vs_NM-NC.txt", treat_group=treat_groups),
        #expand( sample=samples),
'''
rule irf_index:
    input:
        e = soft_dir + "/REF/extra-input-files/RNA.SpikeIn.ERCC.fasta.gz",
        # b = soft_dir + "/REF/extra-input-files/Human_hg19_wgEncodeDacMapabilityConsensusExcludable.bed.gz",
        R = soft_dir + "/REF/extra-input-files/Human_hg19_nonPolyA_ROI.bed",
    output:
        msg = "result/IRFiner_finish.txt",
    params:
        out_dir = soft_dir + "/REF/Human-hg19-release75",
    threads: 5
    shell:"""
        set +u; source ~/miniconda3/bin/activate seq; set -u
        {soft_dir}/bin/IRFinder -m BuildRefProcess -r {params.out_dir} \
            -e {input.e} -R {input.R}
        echo "finish" > {output.msg}
        set +u; conda deactivate; set -u
        """

rule run_irf:
    input:
        index_dir = soft_dir + "/REF/Human-hg38-release81",
        bam = "result/mapping_hg38/{sample}/{sample}_Aligned.out.bam",
    output:
        ir_dir = directory("result/irfinder/{sample}"),
    shell:"""
        set +u; source ~/miniconda3/bin/activate irfinder; set -u
        IRFinder -m BAM -r {input.index_dir} \
            -d {output.ir_dir} {input.bam}
        set +u; conda deactivate; set -u
        """
'''
rule diff:
    input:
        treat = "result/irfinder/{treat_group}/IRFinder-IR-dir.txt",
        ctrl = "result/irfinder/NM-NC/IRFinder-IR-dir.txt",
    output:
        diff_txt = "result/irfinder/{treat_group}_vs_NM-NC.txt",
    shell:"""
        set +u; source ~/miniconda3/bin/activate irfinder; set -u
        {soft_dir}/bin/analysisWithNoReplicates.pl \
            -A {input.treat} -B {input.ctrl} > {output.diff_txt}
        set +u; conda deactivate; set -u
        """
