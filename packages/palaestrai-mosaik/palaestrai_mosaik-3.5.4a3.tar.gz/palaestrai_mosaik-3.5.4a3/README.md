# Adversarial Resilience Learning --- Mosaik Environment

This projects contains the interface between palaestrAI and mosaik, 
the mosaik environment.

## Introduction

This package allows to use worlds created with the co-simulation 
framework mosaik as environment in palaestrAI. The package was 
developed with MIDAS in mind but should work for arbitrary mosaik
worlds. See documenation for more details on how to import a world.

## Installation

palaestrAI-mosaik is written in Python. Use, preferable in a
virtual environment:

```bash
pip install .
```

or, for development including Midas:

```bash
pip install -e .[dev,midas]
```

Alternatively, you can install it from pypi:

```bash
pip install palaestrai-mosaik
```

## Usage

Under tests, you find the `example_experiment_midas.yml` that should be
passed to the palaestrai command line interface::

```bash
palaestrai experiment-start /path/to/tests/example_experiment_midas.yml
```
