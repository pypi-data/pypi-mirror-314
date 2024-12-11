# dsl_dict_analyser

A Python package for analysing dsl dictionaries. Dsl dictionary is a dict type for lingvo app.

## Installation

You can install the package using pip:

```bash
pip install dsl_dict_analyser
```
## Usage

```python

from dictionary_analyser import read
# Read the DSL dictionary file
dsl_dict = read("path/to/dsl_dict.txt")
# then your can read the dsl_dict
# like dsl_dict.cards
# or dsl_dict.name

## Changelog

### 0.0.1 (2024-12-11)
-  Initial release