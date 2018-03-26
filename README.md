# bioscripts

some useful scripts for working with genomics and sequencing data that are stuck in the past (python 2.7)

see also: [bioscripts](https://github.com/christophertbrown/bioscripts)

# installation

`pip install ctbBio27`

## (quick) phylogenetic analysis using ssu_tree.py

Script for quickly generating a 16/18S rRNA gene tree. The script searches a database, usually Silva, for similar reference sequences (choosing the top 3 hits, by default), removes insertions from all sequences, aligns sequences using SSU-Align, combines these sequences with a pre-aligned reference set, and then runs a quick tree using FastTree2. By default, SSU-Align will create separate alignments for sequences from bacteria, archaea, and eukaryotes. In this case, you end up with three separate trees if your sequence set includes sequences from all three domains.

There are options for customizing trees with respect to reference sets and rooting (use -h option for a list).

This is a combination of several scripts that can be used independently for phylogenetic analyses.

`16SfromHMM.py` find ssu rRNA gene sequences (see also `23SfromHMM.py`)

`rax.py` run FastTree and/or RAxML

`search.py` run blast and/or usearch

`numblast.py` get top blast/usearch hits (b6 format)

`stockholm2fa.py` convert stockholm to fasta

`nr_fasta.py` remove sequences in fasta file with same name, or re-name them

`strip_masked.py` remove masked sequence in fasta file

### requirements

* python2.7
* biopython
* tokyocabinet
* [usearch](https://www.drive5.com/usearch/)
* [SSU-Align](http://eddylab.org/software/ssu-align/)
* [FastTree2](http://www.microbesonline.org/fasttree/)
* [RAxML (optional)](https://sco.h-its.org/exelixis/web/software/raxml/index.html)

### example usage

$ ssu_tree.py -i 16S_sequences.fasta

The output will be stored in a directory with a name based on the name of the fasta file you provide. In this case it would be called “16S_sequences.tree". Tree(s) generated will be in this directory and have "FINAL" in the name and end with “.tree".

If you have not identified the 16S genes, you can give the script scaffolds with the --trim option, for example:

$ ssu_tree.py -i sequences.fasta --trim

By default this will include reference sequences and best hits. If you already have your reference set together, you can turn those features off, for example with bacteria sequences:

$ ssu_tree.py -i <unaligned_sequences.fasta> --no-search --no-ref --bacteria

This will align the sequences and run a FastTree. You can also have it run a raxml tree with the --raxml option.

### env. variables for specifying database locations

#### CMs

export ssucmdb="databases/ssu-align-0p1.1.cm"

export lsucmdb="/data1/bio_db/ssu/23S.cm"

#### ssu rRNA gene database (optional)

export ssuref="PATH TO DATABASE FASTA e.g. [Silva](https://www.arb-silva.de)"

#### pre-aligned reference sets (optional)

export ssual_ref_archaea="databases/ssu_refs_archaea-archaea.afa"

export ssual_ref_bacteria="databases/ssu_refs_bacteria-bacteria.afa"

export ssual_ref_eukarya="databases/ssu_refs_eukarya-eukarya.afa"

export ssual_ref_prok_archaea="databases/ssu_refs_prok-archaea.afa"

export ssual_ref_prok_bacteria="databases/ssu_refs_prok-bacteria.afa"

**Note:** include full paths.

## hierarchical taxonomy using id2tax.py

id2tax.py is a script for getting the NCBI hierarchical taxonomy for a lineage based on the name of the lineage, an NCBI TaxID, or an organism GI number.

### requirements

* python2.7 
* tokyocabinet
* "databases" env. variable that specifies the path to where an "ncbi" directory will be created for storing taxonomy databases

### notes

* taxonomy databases are created the first time the script is run (usually takes ~1 day to generate) 
* taxonomy databases are downloaded from NCBI and will need to be updated periodically (delete or move the old databases and re-run id2tax.py)
* for help see `id2tax.py -h`

### example usage:

`$ id2tax.py -i "Bacillus subtilis"`

### or, if you have a list of names in a text file:

`$ cat <list.txt> | id2tax.py -i -`

### output:

Major taxonomic subdivisions are delineated by numbers, and minor subdivisions by semi-colons (if present). You can provide names from any taxonomic subdivision and it will give you the parent lineages. 

There are some funny issues that I have not been able to work out. For example, the name "Bacillus" is redundant in the database, so you will not get the Bacteria taxonomy unless you specify the species name:

`$ id2tax.py -i Bacillus`

Bacillus	[0]Eukaryota;Opisthokonta;Metazoa;Eumetazoa;Bilateria;Protostomia;Ecdysozoa;Panarthropoda;[1]Arthropoda;Mandibulata;Pancrustacea;Hexapoda;[2]Insecta;Dicondylia;[5]Pterygota;Neoptera;Polyneoptera;[3]Phasmatodea;Verophasmatodea;Areolatae;Bacilloidea;[4]Bacillidae;Bacillinae;Bacillini;[5]Bacillus

`$ id2tax.py -i "Bacillus subtilis"`

Bacillus subtilis	[0]Bacteria;Terrabacteria group;[1]Firmicutes;[2]Bacilli;[3]Bacillales;[4]Bacillaceae;[5]Bacillus;[6]Bacillus subtilis group;[6]Bacillus subtilis

Try to watch out for things like this!
