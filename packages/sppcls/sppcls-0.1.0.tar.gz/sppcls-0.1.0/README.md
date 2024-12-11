Python code for working with [the data](https://scm.cms.hu-berlin.de/schluesselstellen/spp-cls-dataexchange/data)
of the DFG-funded [SPP Computational Literary Studies](https://dfg-spp-cls.github.io/).

- **sppcls.py**: the [sppcls](https://pypi.org/project/sppcls/) Python
  module to access the data:
  - blocking:
  ```python
  from sppcls import sppcls
  df = sppcls.load_df(work="judenbuche", projects=["keypassages"])
  print(df.describe())
  ```
  - non blocking:
  ```python
  from sppcls import sppcls
  df = await sppcls.load_df_async(work="judenbuche", projects=["keypassages"])
  print(df.describe())
  ```

## Installation

### PyPI

`pip install sppcls`

or with spacy

`pip install sppcls[spacy]`

### From source

Setup an virtual environment, if necessary:

```sh
python3 -m venv env
source env/bin/activate
```

Install dependencies:

```sh
pip install -r requirements.txt
```

### Note
For tokenization, the spacy model is required:

```sh
python -m spacy download de_core_news_lg
```

## Usage

The package offers a command line interface, either by using the command `sppcls` after installing using PyPI
or `python -m sppcls.cli.sppclscli` when running from source.

```sh
usage: sppclscli.py [-h] {tokenise,check} ...

Accessing and processing data from the DFG-funded SPP Computational Literary
Studies

positional arguments:
  {tokenise,check}
    tokenise        Tokenize text file and create output tsv.
    check           Compare two tsv files and check that the structures
                    matches.

optional arguments:
  -h, --help        show this help message and exit
```

### tokenise

`Tokenise` takes a txt file, e.g. [work.txt](https://scm.cms.hu-berlin.de/schluesselstellen/spp-cls-dataexchange/data/-/blob/main/judenbuche/work.txt),
and produces a tsv file containing the tokenized text, e.g. [work.tsv](https://scm.cms.hu-berlin.de/schluesselstellen/spp-cls-dataexchange/data/-/blob/main/judenbuche/work.tsv).
This base tsv file is then extended by the individual projects.

```sh
usage: sppclscli.py tokenise [-h] input_file output_folder

Tokenize text file and create output tsv.

positional arguments:
  input_file     Path to the input txt file.
  output_folder  Path to the output folder where the output tsv will be saved.

optional arguments:
  -h, --help     show this help message and exit
```

TODO: fix character offset to be byte instead

### check

`check.py` takes two tsv files, e.g. [work.tsv](https://scm.cms.hu-berlin.de/schluesselstellen/spp-cls-dataexchange/data/-/blob/main/judenbuche/work.tsv)
and [keypassages.tsv](https://scm.cms.hu-berlin.de/schluesselstellen/spp-cls-dataexchange/data/-/blob/main/judenbuche/keypassages.tsv),
and makes sure that the project tsv file matches the structure of the base work tsv file.

```sh
usage: sppclscli.py check [-h] org-tokens-file-path project-tokens-file-path

Compare two tsv files and check that the structures matches.

positional arguments:
  org-tokens-file-path  Path to the original tokens tsv file
  project-tokens-file-path
                        Path to the project tokens tsv file

optional arguments:
  -h, --help            show this help message and exit
```
