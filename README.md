# BiT – Bioinformatics Tools for biologist

BiT is a tool for researchers who need to quickly analyze the results of their work: from obtaining complementary nucleic acid to filtering sequences


## Table of contents
[Installation](#installation)

[Available functions](#available-functions)

[System requirements](#system-requirements)

[Contacts](#contacts)

## Installation

To install the BiT, use the following commands:

`git clone git@github.com:opalinn/bit.git`

`cd bit`

## Available functions

### `run_dna_rna_tools`

`transcribe`

Transcribe DNA into RNA. 

If the input sequence is a DNA sequence, it will return the corresponding RNA sequence.

If the input sequence is an RNA sequence, it returns the message: "It is RNA".

`reverse`

Reverses the input sequence. Uses string slicing to create an inverted version of the original sequence. 

`complement`

Generates the complement of the input sequence.

Each nucleotide in the sequence is replaced with its corresponding complement using a predefined dictionary.

`reverse_complement`

Сombination of functions `reverse` and `complement`. 

Returns the reverse complement of the input sequence.

### `filter_fastq`

`filter_by_quality`

Filters sequences based on their quality.

Calculates the average quality of each sequence using the Phred33 scale, and filters them accordingly.

`filter_by_length`

Filters sequences based on their length criteria.

`filter_by_gc_content`

Filters sequences based on the percentage of G and C nucleotides.


## System requirements

**Operating System**: Linux/Mac/Windows

**Python**: Version 3.6 or higher

Also take a healthy nervous system to figure out someone else's code 

## Contacts

If you have any ideas or you encounter a bug, please contact me: pp.malysheva@gmail.com
