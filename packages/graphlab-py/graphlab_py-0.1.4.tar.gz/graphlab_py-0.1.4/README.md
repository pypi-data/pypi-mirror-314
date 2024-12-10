# Graphlab Python SDK

## Installation

Requires Python version `^3.8`:

```bash
pip install graphlab-py
```

## Usage

```py

from graphlab_py import KnowledgeGraph, Ontology, Entity

g = KnowledgeGraph(
    graphdb='falkordb', # only
    language_model='gpt-4o-mini', # any litellm compatible model supported
)
```
