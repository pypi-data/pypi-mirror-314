[![pipeline status](https://gitlab.inria.fr/pydisk/examples/vizitig/badges/main/pipeline.svg)](https://gitlab.inria.fr/pydisk/examples/vizitig/-/commits/main) 
[![coverage report](https://gitlab.inria.fr/pydisk/examples/vizitig/badges/main/coverage.svg)](https://gitlab.inria.fr/pydisk/examples/vizitig/-/commits/main) 
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)


Vizitig is:

- A command line interface (CLI) to administrate, build and annotate genomic or transcriptomic graph and update them
- A Web interface to vizualize and manipulate those graphs
- A Python library for a programmatic pythonic interaction with graphs

# Installation

`Vizitig` can be installed as 

```bash
pip install vizitig
```

This should work for major distributionss.
It is however mostly battle tested on Linux. 

Some system (as debian) will prevent you to run this
command as it could be incompatible with your system
Python librairie. To avoir the issue, you should run
the command [within a virual environnement](https://docs.python.org/3/library/venv.html)


## Vizitig custom binaries

Some part of Vizitig are pre-compiled librariries written on rust. This library will be automatically installed on your computer if you have cargo installed. This library is valled Vizibridge. Vizitig should run wihtout it but it will be vastly slower on build and annotation task. Additionnal indexes are provided by this library. 
To check if vizibridge is installed you can run

```
pip show vizibridge
``` 

If it is not installed, you can install vizibridge for your system
with the following script. Be aware that this will install the full rust
compilation tool chain.

The following script assumes `pip` and `venv` are already installed.


TODO: check the script.

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source ~/.bashrc # this is to refresh the path 
cargo install maturin
python3 -m venv venv
source venv/bin/activate
git clone https://gitlab.inria.fr/cpaperma/vizibridge
cd vizibridge; maturin build --release
pip install target/wheels/vizibridge**.whl
cd ..;git clone https://gitlab.inria.fr/pydisk/examples/vizitig
cd vizitig
pip install .[all]
```

# The CLI

Before running any CLI command, you should activate the virtual environment in which Vizitig runs. 
To do so, you can type the following while in the vizitig folder: 

```bash
source venv/bin/activate
```

The CLI is rather self contained with documentation:

```
vizitig -h
```

Will provides the following:

```
usage: vizitig [-h] {info,rename,add,rm,search,update,annotate,build,genes,run} ...

A CLI interface to vizitig

positional arguments:
  {info,rename,add,rm,search,update,annotate,build,genes,run}
    info                get information about ingested graphs
    rename              Rename a graph
    add                 Add an already built Vizitig Graph
    rm                  Remove an already built Vizitig Graph
    update              update a graph
    annotate            Add gene annotation to a given graph
    build               build a new graph from BCALM file
    genes               Add gene annotation to a given graph
    run                 run Vizitig locally

usage: Vizitig [-h] {info,build,run,update} ...

```

Each subcommand has its own help. 

## Environnement variables

It is possible to use environnement variables to change the global
behavor of vizitig:

- VIZITIG_PYTHON_ONLY: if set ot any value, do not use vizibridge (compiled binaries)
- VIZITIG_DEFAULT_SHARD_NB: set the default shard number in building index (default is computed with amount of CPUs)
- VIZITIG_DEFAULT_INDEX: set the default index type choosen.
- VIZITIG_DIR: set the main data directory of vizitig (default is in ~/.vizitig).
- VIZITIG_TMP_DIR: set the temporay data directory of vizitig (default to the choice of tempfile standard module on the system).
- VIZITIG_NO_TMP_INDEX: if set, will not use temporary index when performing some annotation operation 


# Client based interaction

To launch the web client use the following command.

```
vizitig run
```

It should open the webclient.

To build a new graph to the application run (still within the venv)

```
vizitig build /path/to/some/bcalm/file
```

with k being the size of the kmers. We recommand using k = 21. The compiled version will work for k < 63.

For instance

```
vizitig build my_bcalm.fa 
```

or 

```
vizitig build my_bcalm.fa  --k 21 -n my_awesome_graph
```

It can take some time and some space on the disk (but should not use too much memory).

To get some information about ingested graphs, simply run

```
vizitig info
```

## The vizitig query language

While in the web user interface, a query field is available. Two execution modes are available for the queries. After typing a query, you can : 
- Execute this query on the graph. To do so, click on the "Fetch nodes" green buttons. This will fetch all the corresponding nodes from the database to the user interface (from the disk to the RAM) and materialise the nodes in the user interface.
- Execute this query on the loaded nodes. To do so, click on the "Add filter" blue button, name your filter and add it. Now, in any visualisation instance, you can click on "Add action" and select your filter. This action will only apply to loaded nodes. If you load new nodes, the actions will be applied to them. 

In the CLI, only the first mode is available. Instead of materialising the nodes, the CLI will return a list of nodes IDs. 

The query language is really simple. It contains 3 operators : AND, OR and NOT. Those are logical operators that correspond to conjunction, disjunction, and complement. Their meaning may diverge from what we expect in the current language. We suggest you look at [this page](https://en.wikipedia.org/wiki/Boolean_algebra) if you are not familiar with the concepts of mathematical logic. The Venn diagramm in the section "Diagrammatic representations" sums things up nicely enough. 

Operators can be used between or in front of formulas. In our case, formulas are composed of the name of the metadata (see the section annotations for more details on annotation) you want to query plus its name in parenthesis.

Query for all the nodes that are tagged with the gene DRA_012 : 
```
Gene(DRA_012)
```

Query for all the nodes that are not tagged with this metadata : 
```
NOT Gene(DRA_012)
```

Query for the nodes in the sample 1 or in the sample 2 : 
```
Color(sample1) OR Color(sample2)
```

Query for the nodes in the sample 1 and in the sample 2 (here nodes have to be shared by the 2 samples):
```
Color(sample1) AND Color(sample2)
```

Parenthesis can be used in the process. Query blocs in parenthese will work just like a classic metadata query. 
For instance, if you want all the nodes that are in the sample 1 or in the sample 2 but not in the sample 3 : 
```
(Color(sample1) OR Color(sample2)) AND NOT Color(sample3)
``` 

Knowing what to type to find a precise metadata may be complicated if you have tricky data, so we built a metadata explorer that you can open in the visualisation by clicking the blue metadata button. First, choose the type of metadata that you want to see and then click on the button corresponding to this metadata. It will add the right query for it in the query field. All that remains to be done is typing the logical operators and the parenthesis to have a functionnal query. 

# Graph Annotations

To color a graph (that is to mark some node of the graph with some metadata)
you can use the `update` subcommand. This command is tought to allow users to keep track of the origin sample of one data. It differs from the other annotation features that we explain below, because it only requires a reference sequence and no annotation data.

We advise you to use the a graph file as input for this command, eventough a classic fasta or fna file will generally work as well. 

The recommended workflow is the following:

- Build a graph with all your sequences. You can easily build the DBG graph of several sequences using [ggcat](https://github.com/algbio/ggcat).
- Use Vizitig build to ingest the graph in Vizitig. 
- Use Vizitig update with your initial sequences (or their graph) to keep track of the origin sample or each sequence. 

```bash
vizitig update -h
```

```bash
usage: vizitig update [-h] -m name [-d description] [-k file [file ...]] [-b buffer] [-u url [url ...]] [-c color] graph

positional arguments:
  graph                 A graph name. List possible graph with python3 -m vizitig info

options:
  -h, --help            show this help message and exit
  -m name, --metadata-name name
                        A key to identify the metadata to add to the graph
  -d description, --metadata-description description
                        A description of the metadata
  -k file [file ...], --kmer-files file [file ...]
                        Path toward files containing kmers (fasta format)
  -b buffer, --buffer-size buffer
                        Maximum size of a buffer
  -u url [url ...], --kmer-urls url [url ...]
                        URLs toward files containing kmers (fasta format)
  -c color, --color color
                        Default color to use in the vizualisation. Default is None
```

The typical usage would be :

```
vizitig update -k my/awesome/file.fa -d "This contains some cure against the cancer somehow" -m "sample1" my_graph_name
```

After this, you will be able to fetch all the nodes of the graph that correspond to this sample by using the following query :
```
Color(sample1)
```

More complex options exist to add metadata to a graph. One is suited for transcriptomic references, the other for genomic references. 

### Transcriptomic 

To add metadata with transcriptomic references, use Vizitig genes. 
```
Vizitig gene -h 
```

```
usage: vizitig genes [-h] -r refseq -m gtf [-p] graph

positional arguments:
  graph                 A graph name. List possible graph with python3 -m vizitig info

options:
  -h, --help            show this help message and exit
  -r refseq, --ref-seq refseq
                        Path toward a (possibly compressed) fasta files containing reference sequences
  -m gtf, --metadata gtf
                        Path towards a (possibly compressed) gtf files containing metadata of reference sequences
  -p, --parse-only      Go through the data without ingesting. Provides the number of line to ingest
```

The typical usage would be : 
```
vizitig genes -r my_data/transcript_ref.fa -m my_data/transcript_annot.gtf my_graph
```

Vizitig will proceed with the following : for each metadata line found in transcript_annot.gtf, it will look for a reference transcript or gene in the transcript_ref.fa file. If found, it will tag all the nodes that correspond to the reference sequence with the metadata. 

If your gtf files contains a Transcript with id NM_010111, you can query the corresponding nodes with the query : 
```
Transcript(NM_010111)
```

### Genomic
To add metadata with genomic references, use Vizitig annotate. 
```
Vizitig annotate -h 
```

```
usage: vizitig genes [-h] -r refseq -m gtf [-p] graph

positional arguments:
  graph                 A graph name. List possible graph with python3 -m vizitig info

options:
  -h, --help            show this help message and exit
  -r refseq, --ref-seq refseq
                        Path toward a (possibly compressed) fasta files containing reference sequences
  -m gtf, --metadata gtf
                        Path towards a (possibly compressed) gtf files containing metadata of reference sequences
```

The typical usage would be : 
```
vizitig annotate -r my_data/genome_ref.fa -m my_data/annot.gtf my_graph
```

Vizitig will proceed with the following : for each metadata line found in annot.gtf, it will look for the sequence in the reference file. When found, it will tag all the nodes that correspond to the reference sequence with the metadata.

If your gtf files contains a Exon with id DRA_0172, you can query the corresponding nodes with the query : 
```
Exon(DRA_0172)
```


## Running a small example

Vizitig comes with a set of data that can be used to explore the tool.
By default, the `mini_bcalm.fa` is available.

To use this example, go in your vizitig folder using a command line tool, activate the venv and run vizitig.

Assuming your vizitig folder is situated in your home folder and you opened a terminal in your home folder (otherwise change the path), you can run: 

```
cd vizitig 
```

to go in your vizitig folder. 

Then: 

```
source venv/bin/activate
```

will activate the venv (virtual environment) to allow vizitig and all its dependencies to run. 

Then: 

```
make small_ex
```

will build the graph, update it with origin sequences and add the gene annotations. This command calls the make_file part of the Makefile file, that executes the build, update and genes commands. 

To use vizitig, you can finally run 

```
vizitig run
```

A webapp will open and you can select the mini_bcalm graph. You can select the genes, or the transcripts that you want to display to have a targeted visualisation.

In any case, as soon as a graph node is displayed, you can unfold every neighboor node from the currently displayed nodes. 

## Removing graphs 
You can delete a graph from the web interface, but also in command line : 

With the venv activated and in the vizitig folder, you can remove a graph by using the following command:
```bash
make remove_graph GRAPH="name_of_the_graph" #Name of the graph without extension
```
Or you can remove all the graphs by using 
```
make remove_all_graphs
```

For instance, deleting the mini_bcalm.fa graph would require the following line:
```
make remove_graph GRAPH="mini_bcalm.fa"
```

Please note that you may need to run the commands as administrator if you encounter a permission denied error: 

```bash
(venv) user@Machine:~/vizitig$ make remove_all_graphs
rm -rf /home/user/.vizitig/data/*
rm: cannot remove '/home/user/.vizitig/data/*': Permission denied

#Execute as administrator using sudo
(venv) user@Machine:~/vizitig$ sudo make remove_all_graphs
rm -rf /home/user/.vizitig/data/*
(venv) user@Machine:~/vizitig$ #Operation successful
```

## Running a coloring example using fasta data - covid example

This sections aims at giving the users the possibility to build an exemple by themselves from A to Z. We provide the data. 

To run this example, you will need to download the following files :
[click here](https://zenodo.org/records/11192088?token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6ImJhZWY4Zjk4LTAxNmItNDkzMi05YmMxLTFlZjQ0MDdkYzRhMiIsImRhdGEiOnt9LCJyYW5kb20iOiI3MGU3MWJhOWZhNWZhYzcxZTc3OGU2MDg1ZDc5ZjIxNCJ9.i9wGjOBGVEiuc8F7U65lvhRgLHF4a9zsfjzj8fimP_cT8HK4_Mds_ZBSGeyLtJkF9WkNHV6jW7rgz5JUUGPEZQ).

Please note that we do not claim owernship of the data, nor the relevance of the data naming. 
This data set was created for the purpose of showing a small existing example only. 

You can also conduct the same process with your own files. 

We will build a new graph from four fasta file. In our cases, they are named:

- SARS_CoV_alpha.fna
- SARS_CoV_beta.fna
- SARS_CoV_Spike_alpha.fna
- SARS_CoV_Spike_beta.fna

This dataset is composed of alpha and beta covid, as well as their associated spike proteins. 

Open a terminal in the vizitig folder.

1. Build a graph with our files\
The first step is to build a bcalm graph. We advise to use [ggcat](https://github.com/algbio/ggcat). The following command takes as input the fasta files.


```
ggcat build data/covid/SARS_CoV_* -e -s 1 --kmer-length 21 -o data/covid_example
```

The "SARS_CoV_*"  parameter means "all files that start by SARS_CoV_", in our case all the files (because we named them accordingly). 


The ```-e``` and ```-s``` parameters are really important, as they allow ggcat to build the edges of our graph.

2. Launch the vizitig environement.
*Make sure to be in the parent folder of the vizitig and data folder with your command line tool.*
```
source vizitig/venv/bin/activate
cd vizitig
```

3. Ingest the graph inside vizitig

```
vizitig build ../data/covid_example -n covid_example
```

3. Build the index for the graph 

```
vizitig index build covid_example
```

5. Update the graph with the genomes

We update the graph with the initial sequences. Therefore the graph will be tagged with 4 colors, and we will be able to see the origin sequence of each node. 

```
vizitig update -k ../data/covid/SARS_CoV_alpha.fna -m "Covid_Alpha" covid_example
vizitig update -k ../data/covid/SARS_CoV_beta.fna -m "Covid_Beta" covid_example
vizitig update -k ../data/covid/SARS_CoV_Spike_alpha.fna -m "Spike_Protein_Alpha" covid_example
vizitig update -k ../data/covid/SARS_CoV_Spike_beta.fna -m "Spike_Protein_Beta" covid_example
```


6. Launch vizitig

```
vizitig run
cd ../
```

7. Use vizitig

You can now select your graph "example_covid" on the top-left part. You can search for a specific sub-sequence of kmer and unfold the graph. Several visualisation types are opened by default. You can reopen them using the visualisation menu. 


# Vizitig as librairy 

Most of graph operation are directly accessible directly with a Python. It is a thin wrapper
around `NetworkDisk` which is `NetworkX` on disk implementation, storing graphs in a normalized way into a database.

```python
from vizitig import info as vizinfo
L = vizinfo.graphs_list() # get the list of available graph
d = vizinfo.graph_info(L[0]) # return a dict with information about the graph
G = vizinfo.get_graph(L[0]) # get the networkdisk graph
```

You can also get a graph directely by its name. You cannot give a name to your vizitig graph when you build it yet (the name of the ggcat graph will be taken by default) but you can see all the names of the graphs by running 
```
vizitig info
```
in the venv.
If you know the name of your graph, you can also access it using the following method: 

```python
from vizitig import *
G = get_graph('name_of_your_graph') #name of the graph without extension
```

For the mini bcalm graph provided in vizitig, it would be: 
```python
from vizitig import *
G = get_graph('mini_bcalm.fa') #the extension is .db, .fa remains from the ggcat graph
```

Metadata are stored within the Graph data and are also accessible:

```python
GM = G.metadata # the description and list of all metadata
GM.color_list # list of all the sequences your colored your graph with
```

To save space in the graph, nodes labeled by the metadata contain
the key `i`. For instance:

```python
G.find_all_nodes(0) # return all the nodes tagged with G.graph["meta_list"][0]
```

You can also search for a precise kmer as follows:

```python
G.find_one_node("GCTGCT...ACGT")
```

Or you can fetch all nodes that contains a subsequence as follows:

```
G.find_all_node(seq=lambda e:e.like("%TGCAGCAC%"))
```

The last one will perform a sequential scan over the database as it is not indexed,
so it will be rather slow. All the other query are performed with an appropriate
index accelerating them.
This means that searching for a kmer is way faster than searching by a sequence. 


## Compiled binary included

Some part of `Vizitig` are compiled and packaged through the `vizibridge`
module.  This module can be toggle off and backtracked to a pure Python
implementation by setting up the environnement variable VIZITIG_PYTHON_ONLY` to
any non empty value.  Part of the optimizations provided by vizibridge are the
sequence computations (for instance the enumeration of the kmers of a
sequence). The performances improvement are considerable on middle to high
sized graph but are limited to Linux with x86_64 machine for now.

