def bedgraph_file_processer(annotation_file, bedgraph_file, output_file):
    with open(output_file, mode="w") as output:
        with open(annotation_file, mode="r") as annot:
            for line in annot:

                chrom, start, end, strand, gene = line.split()
                start, end = int(start), int(end)

                summary_signal = 0

                with open(bedgraph_file, mode="r") as bedgr:
                    for line in bedgr:
                        chrom_2, start_2, end_2, sig_value = line.split()
                        start_2, end_2, sig_value = (
                            int(start_2),
                            int(end_2),
                            float(sig_value),
                        )

                        if chrom == chrom_2 and (start_2 - 1 >= start and end_2 <= end):
                            summary_signal += sig_value

                output.write(
                    f"{chrom}\t{start}\t{end}\t{gene}\t{strand}\t{summary_signal}\n"
                )


annotation_file = "annotation_genes.txt"
bedgraph_file = "gerp_data.bedGraph"
output_file = "output_1_try.txt"

bedgraph_file_processer(annotation_file, bedgraph_file, output_file)
