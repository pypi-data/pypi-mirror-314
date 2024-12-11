---
title: README
---

# Synopsis

A wrapper around the [UniProt ID Mapping web service](https://www.uniprot.org/help/id_mapping) with local caching to speed up subsequent queries and reduce server load. The package provides both a Python library and a command-line utility for mapping IDs between any of the supported databases.

# Links

[insert: links]: #

## GitLab

* [Homepage](https://gitlab.inria.fr/jrye/uniprot-id-mapping)
* [Source](https://gitlab.inria.fr/jrye/uniprot-id-mapping.git)
* [Documentation](https://jrye.gitlabpages.inria.fr/uniprot-id-mapping)
* [Issues](https://gitlab.inria.fr/jrye/uniprot-id-mapping/-/issues)
* [GitLab package registry](https://gitlab.inria.fr/jrye/uniprot-id-mapping/-/packages)

## Other Repositories

* [Python Package Index](https://pypi.org/project/uniprot-id-mapping/)

[/insert: links]: #

# Usage

## Python API

~~~python
# Import the IdMapper class.
from uniprot_id_mapping import IdMapper

# Instantiate it.
id_mapper = IdMapper()

# Create a list or other iterable of IDs.
ids = ["P21802", "P12345"]

# Get a dict mapping the given IDs from UniProtKB_AC-ID to UniRef90.
mapped = id_mapper.map_ids("UniProtKB_AC-ID", "UniRef90", ids)

# Get the JSON object containing the information about available fields.
fields = id_mapper.fields
~~~

For further details, please see the API documentation linked above.


## Command-Line Utility

The package installs the command-line utillity `uniprot-id_mapper` which can be used to map IDs from command-line arguments or input files. The results can be printed in plain test or as JSON. The utility also provides subcommands for managing the cached results and listing available databases.

[insert: command_output uniprot-id_mapper -h]: #

~~~
usage: uniprot-id_mapper [-h] [--cache-dir CACHE_DIR] [-j] [-t TIMEOUT] [-v]
                         {map,list,clear} ...

Map IDs between databases using UniProt's ID Mapping service.

positional arguments:
  {map,list,clear}
    map                 Map given IDs from one database to another
    list                List available "from" and "to" databases.
    clear               Clear the cache. If you only wish to clear missing
                        identifiers, use the --clear-missing option of the
                        "map" command.

options:
  -h, --help            show this help message and exit
  --cache-dir CACHE_DIR
                        A directory for caching results locally. If not given,
                        a standard path will be used.
  -j, --json            Output results in JSON.
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout for establishing remote connections.
  -v, --verbose         Increase logging level to DEBUG.

~~~

[/insert: command_output uniprot-id_mapper -h]: #

### Map

[insert: command_output uniprot-id_mapper map -h]: #

~~~
usage: uniprot-id_mapper map [-h] [--id-list ID_LIST] [--refresh-missing]
                             from to [id ...]

positional arguments:
  from               The database of the given IDs.
  to                 The target database to which to map the given IDs.
  id                 The IDs to map.

options:
  -h, --help         show this help message and exit
  --id-list ID_LIST  Path to a file with a list of IDs, one per line.
  --refresh-missing  Query the server for previously missing identifiers
                     instead of using cached values.

~~~

[/insert: command_output uniprot-id_mapper map -h]: #

### List

#### Help Message

[insert: command_output uniprot-id_mapper list -h]: #

~~~
usage: uniprot-id_mapper list [-h]

options:
  -h, --help  show this help message and exit

~~~

[/insert: command_output uniprot-id_mapper list -h]: #

#### Example Output

[insert: command_output uniprot-id_mapper list]: #

~~~
From
  Allergome
  ArachnoServer
  Araport
  BioCyc
  BioGRID
  BioMuta
  CCDS
  CGD
  CPTAC
  CRC64
  ChEMBL
  ChiTaRS
  CollecTF
  ComplexPortal
  ConoServer
  DIP
  DMDM
  DNASU
  DisProt
  DrugBank
  EMBL-GenBank-DDBJ
  EMBL-GenBank-DDBJ_CDS
  ESTHER
  EchoBASE
  Ensembl
  Ensembl_Genomes
  Ensembl_Genomes_Protein
  Ensembl_Genomes_Transcript
  Ensembl_Protein
  Ensembl_Transcript
  FlyBase
  GI_number
  GeneCards
  GeneID
  GeneReviews
  GeneTree
  GeneWiki
  Gene_Name
  GenomeRNAi
  GlyConnect
  GuidetoPHARMACOLOGY
  HGNC
  HOGENOM
  IDEAL
  KEGG
  LegioList
  Leproma
  MEROPS
  MGI
  MIM
  MaizeGDB
  OMA
  OpenTargets
  Orphanet
  OrthoDB
  PATRIC
  PDB
  PHI-base
  PIR
  PeroxiBase
  PharmGKB
  PlantReactome
  PomBase
  ProteomicsDB
  PseudoCAP
  REBASE
  RGD
  Reactome
  RefSeq_Nucleotide
  RefSeq_Protein
  SGD
  STRING
  SwissLipids
  TCDB
  TreeFam
  TubercuList
  UCSC
  UniParc
  UniPathway
  UniProtKB_AC-ID
  UniRef100
  UniRef50
  UniRef90
  VEuPathDB
  VGNC
  WBParaSite
  WBParaSite_Transcript-Protein
  WormBase
  WormBase_Protein
  WormBase_Transcript
  Xenbase
  ZFIN
  dictyBase
  eggNOG
  euHCVdb
  neXtProt

To
  Allergome
  ArachnoServer
  Araport
  BioCyc
  BioGRID
  BioMuta
  CCDS
  CGD
  CPTAC
  CRC64
  ChEMBL
  ChiTaRS
  CollecTF
  ComplexPortal
  ConoServer
  DIP
  DMDM
  DNASU
  DisProt
  DrugBank
  EMBL-GenBank-DDBJ
  EMBL-GenBank-DDBJ_CDS
  ESTHER
  EchoBASE
  Ensembl
  Ensembl_Genomes
  Ensembl_Genomes_Protein
  Ensembl_Genomes_Transcript
  Ensembl_Protein
  Ensembl_Transcript
  FlyBase
  GI_number
  GeneCards
  GeneID
  GeneReviews
  GeneTree
  GeneWiki
  Gene_Name
  GenomeRNAi
  GlyConnect
  GuidetoPHARMACOLOGY
  HGNC
  HOGENOM
  IDEAL
  KEGG
  LegioList
  Leproma
  MEROPS
  MGI
  MIM
  MaizeGDB
  OMA
  OpenTargets
  Orphanet
  OrthoDB
  PATRIC
  PDB
  PHI-base
  PIR
  PeroxiBase
  PharmGKB
  PlantReactome
  PomBase
  ProteomicsDB
  PseudoCAP
  REBASE
  RGD
  Reactome
  RefSeq_Nucleotide
  RefSeq_Protein
  SGD
  STRING
  SwissLipids
  TCDB
  TreeFam
  TubercuList
  UCSC
  UniParc
  UniPathway
  UniProtKB
  UniProtKB-Swiss-Prot
  UniRef100
  UniRef50
  UniRef90
  VEuPathDB
  VGNC
  WBParaSite
  WBParaSite_Transcript-Protein
  WormBase
  WormBase_Protein
  WormBase_Transcript
  Xenbase
  ZFIN
  dictyBase
  eggNOG
  euHCVdb
  neXtProt


~~~

[/insert: command_output uniprot-id_mapper list]: #

### Clear

[insert: command_output uniprot-id_mapper clear -h]: #

~~~
usage: uniprot-id_mapper clear [-h]

options:
  -h, --help  show this help message and exit

~~~

[/insert: command_output uniprot-id_mapper clear -h]: #
