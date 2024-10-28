# Project 1. What causes antibiotic resistance? Alignment to reference, variant calling 

Authors: Basova Victoria, Malysheva Polina

## Table of content

[Part 1. Get and check data](pPart-1.-Get-and-check-data)

[Part 2. Inspect raw sequencing data with FastQC](#part-2.-Inspect-raw-sequencing-data-with-FastQC)

[Part 3. Filtering the reads](#part-3.-Filtering-the-reads)

[Part 4. Aligning sequences to reference](#part-4.-Aligning-sequences-to-reference)

[Part 5. Variant calling](#part-5.-Variant-calling)

[Part 6. Automatic SNP annotation](#part-6.-Automatic-SNP-annotation)

## Part 1. Get and check data

Download:

- reference genome of E.coli strain K-12 substrain MG1655 (.fna.gz)

- genome annotation in (*_genomic.gff.gz)

- raw Illumina reads of an E. coli strain that is resistant to the antibiotic ampicillin (two .fastq.gz)

Check manually that files are correct:

- look at the first 20 lines in file:
  
`head -20 filename.format`

.fastq and .fasta are different! 

- count reads in each fastq file:
  
```bash
wc -l filename.fastq
```

In `amp_res_1.fastq.gz` there are 455876 reads and the same number of reads in the `amp_res_2.fastq.gz`, because we have pair-end sequencing

Check our data with seqit:

```bash
seqkit stats filename
```

Stats for amp_res_1.fastq.gz (same for amp_res_2.fastq.gz): 

- num_seqs: 455,876

- min_len: 101

- avg_len: 101

- max_len: 101

## Part 2. Inspect raw sequencing data with FastQC

Run FastQC:

```bash
fastqc -o path/to/output_dir /path/to/file/file.fastq
```

It produce two .html reports for each file. 

Let's look for one report:

- Basic Statistics. Total Sequences is the same as we calculated above. 
  
![image](https://github.com/user-attachments/assets/b25fc13f-16a0-45f1-a002-8357a676f3a9)

- Per base sequence quality. The quality of the read decreases towards the end, as the chemical reagents may degrade during the process of sequencing.

![image](https://github.com/user-attachments/assets/7513cb08-36d2-4c9f-9d68-e7e327a28ae6)

- Per tile sequence quality. We see red and yellow zones. This indicates a problem related to the substrate on which the sequencing is taking place. There was probably debris, dust, or air bubbles.

![image](https://github.com/user-attachments/assets/1b921bb1-ee40-4a6d-9f84-b75e3db774fc)

- Per base sequence content. At the beginning of the reads there are jumps that may be associated with the start of sequencing and annealing of primers

![image](https://github.com/user-attachments/assets/e20dd674-0190-4522-af7b-ecc9c39e39e1)

-  Overrepresented sequences. Nothing was detected. 

If we see something unusual in the FastQC report, we need to think about sample preparation and sequencing itself. If we had an unusual distribution of GC content, 
this would require contamination of our samples. In our case, we had problems with the tile. Most likely, it was not washed well after application or was stored in 
poor conditions, and dust got on it.

## Part 3. Filtering the reads

Вика, вставь, пожалуйста, скрины фасткуси после триммоматика

Let's remove reads with poor quality and trim them from the end and from the beginning to improve the overall quality of the reads with Trimmomatic.

``` bash
trimmomatic PE -phred33 amp_res_1.fastq.gz amp_res_2.fastq.gz amp_res_1_P.fastq.gzamp_res_1_U.fastq.gz amp_res_2_P.fastq.gz amp_res_2_U.fastq.gz
LEADING:20 TRAILING:20 SLIDINGWINDOW:10:20 MINLEN:20
```

Statistics after trimming and filtering reads:

Input Read Pairs: 455876 

Both Surviving: 446259 (97,89%) 

Forward Only Surviving: 9216 (2,02%) 

Reverse Only Surviving: 273 (0,06%) 

**Dropped: 128 (0,03%)** 

If we increase the quality score at all steps to 30, we will filter out more reads and fewer reads will go into analysis

Input Read Pairs: 455876 

Both Surviving: 446200 (97.88%) 

Forward Only Surviving: 9243 (2.03%) 

Reverse Only Surviving: 291 (0.06%) 

**Dropped: 142 (0.03%)**

## Part 4. Aligning sequences to reference

### Index the reference file:

```bash
bwa index GCF_000005845.2_ASM584v2_genomic.fna.gz 
```

It produce files:

- GCF_000005845.2_ASM584v2_genomic.fna.gz.amb				 

- GCF_000005845.2_ASM584v2_genomic.fna.gz.ann					 

- GCF_000005845.2_ASM584v2_genomic.fna.gz.bwt					 

- GCF_000005845.2_ASM584v2_genomic.fna.gz.pac					 

- GCF_000005845.2_ASM584v2_genomic.fna.gz.sa

### Align reads:

```bash
bwa mem GCF_000005845.2_ASM584v2_genomic.fna.gz amp_res_1_P.fastq.gz amp_res_2_P.fastq.gz > alignment.sam 
```

And compress and sort the sam file. A compressed sam file is called a bam file.

```bash
samtools view -S -b alignment.sam > alignment.bam 
```

Let's look at statistics after alignment:

```bash
samtools flagstat alignment.bam  
892776 + 0 in total (QC-passed reads + QC-failed reads) 
892518 + 0 primary 
0 + 0 secondary 
258 + 0 supplementary 
0 + 0 duplicates 
0 + 0 primary duplicates 
891649 + 0 mapped (99.87% : N/A) 
891391 + 0 primary mapped (99.87% : N/A)
892518 + 0 paired in sequencing 
446259 + 0 read1 
446259 + 0 read2 
888554 + 0 properly paired (99.56% : N/A) 
890412 + 0 with itself and mate mapped 
979 + 0 singletons (0.11% : N/A) 
0 + 0 with mate mapped to a different chr 
0 + 0 with mate mapped to a different chr (mapQ>=5)
```
99.87% of reads are mapped. 

### Sort and index BAM file

```bash
samtools sort alignment.bam -o alignment_sorted.bam 
samtools index alignment_sorted.bam  
```
This produced alignment_sorted.bam.bai file.

### Explore visualization in Unipro UGENE 

To do this you need two files in launch folder: sorted .bam and index .bai 

![image](https://github.com/user-attachments/assets/b5c16445-60b7-4704-bd69-72cb691c3662)

## Part 5. Variant calling

Let's make .mpileup intermediate file for VarScan: 

```bash
samtools mpileup -f GCF_000005845.2_ASM584v2_genomic.fna alignment_sorted.bam > my.mpileup 
```

To call actual variants, we will use VarScan with 50% threshold because we had a pure culture of bacteria whose genome was sequenced

```bash
varscan mpileup2snp my.mpileup --min-var-freq 0.5 --variants --output-vcf 1 > VarScan_results.vcf 
```

## Part 6. Automatic SNP annotation

To annotate vcf file, we need sequence and annotation of our reference, to build a custom database use snpEff tool. 

1. Download GCF_000005845.2_ASM584v2_genomic.gbff.gz

2. Create empty file snpEff.config and put it to `data/k12` folder with unziped .gbk file

3. Create database
   
```bash
snpEff build -genbank -v k12
```

4. Annotate
   
```bash
snpEff ann k12 VarScan_results.vcf > VarScan_results_annotated.vcf
```
After this we obtained a vcf file with additional field "ANN" (for "annotation"), describing all the effects for each SNP.


