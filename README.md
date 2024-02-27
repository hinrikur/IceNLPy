[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-3817/)
![PyPI](https://img.shields.io/pypi/v/icenlpy)

# IceNL*Py*

#### 🐍 A Python wrapper for IceNLP

Ever wanted to use [IceNLP](https://clarin.is/en/resources/icenlp/) with the ease of any other Python package? Now you can!

**IceNL*Py*** is a Python wrapper for the Java-based IceNLP toolkit for Icelandic. Although originally made for fun, the package is fully functional and can be used in real-world projects.

## Usage

### In Python:

```python

>>> from icenlpy import icetagger, iceparser, tokenizer

>>> text = "Hann er mjög virtur málfræðingur að norðan. Hvað segirðu um það?"
>>> tokens = tokenizer.split_into_sentences(text)
>>> tokens

['Hann er mjög virtur málfræðingur að norðan .', 'Hvað segirðu um það ?']

>>> tagged = icetagger.tag_text(tokens)
>>> tagged

['Hann fpken er sfg3en mjög aa virtur lkensf málfræðingur nken að aa norðan aa . .\n', 
'Hvað fshen segirðu sfg2en um ao það fpheo ? ?\n']

>>> parsed = iceparser.parse_text(tagged)
>>> parsed

[[[NP Hann fpken ] [VPb er sfg3en ] [NP [AP [AdvP mjög aa ] virtur lkensf ] málfræðingur nken ]
[AdvP að aa norðan aa ] . .], [[NP Hvað fshen ] [VP segirðu sfg2en ] [PP um ao [NP það fpheo ] ] ? ?]]

>>> for sent in parsed:
...     print(f"Sentence text: {sent.text}\n")
...     print(sent.view)

Sentence text: Hann er mjög virtur málfræðingur að norðan .

S0
+-NP
  +-fpken: 'Hann'
+-VPb
  +-sfg3en: 'er'
+-NP
  +-AP
    +-AdvP
      +-aa: 'mjög'
    +-lkensf: 'virtur'
  +-nken: 'málfræðingur'
+-AdvP
  +-aa: 'að'
  +-aa: 'norðan'
+-.: '.'

Sentence text: Hvað segirðu um það ?

S0
+-NP
  +-fshen: 'Hvað'
+-VP
  +-sfg2en: 'segirðu'
+-PP
  +-ao: 'um'
  +-NP
    +-fpheo: 'það'
+-?: '?'
```

### CLI:

The package also includes a basic command line tool to use the tools from the terminal. The tokenizer command is shown below:

**Input:**

```bash
$ icenlpy tokenizer --help
```

**Output:**

```bash

usage: icenlpy tokenizer [-h] [-i INPUT] [-o OUTPUT] [-of {1,2}] [-t] [input_text]

positional arguments:
  input_text            Direct text to process

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file path
  -o OUTPUT, --output OUTPUT
                        Output file path
  -of {1,2}, --output-format {1,2}
                        The desired output format. 1 for one token per line, 2 for one sentence per line.
  -t, --tree-view       Print the output in a tree view format. Only applies to IceParser.


$ icenlpy tokenizer "Hann er mjög virtur málfræðingur að norðan." -of 1

Hann
er
mjög
virtur
málfræðingur
að
norðan
.
```

## Features

The package is designed to be as simple as possible, and integrate well into established workflows in NLP projects which use purely Python-implemented packages, e.g. [GreynirEngine](https://github.com/mideind/GreynirEngine) for Icelandic or [spaCy](https://spacy.io/) for other languages. Dependencies are kept to a minimum outside the Python standard library and the IceNLP Java library itself.

With this in mind the package is distributed with the original IceNLP JAVA clusters, and interacts with them using simple I/O calls via the `subprocess` module. This is simple and lightweight, but has not been tested for specifically for performance or scalability.

As of pre-release version 0.1.7, the package supports the following features:

- Tokenization via the `tokenizer` module
- Part-of-speech tagging via the `icetagger` module
- Parsing via the `iceparser` module

Along with the built-in features of IceNLP, the package also includes a simple way to convert IceNLP output to a more human-readable format, and dedicated object types to better manipulate the output in external pipelines. As such, it emulates the functionality of more modern NLP toolkits, particularly GreynirEngine.

Future version of the package may include additional features, such as named entity recognition and lemmatization.

## About

IceNLP, a groundbreaking NLP library for Icelandic was developed by Hrafn Loftsson from 2004 to 2007, with sporadic modifications and expansions in the mean time by students at the University of Reykjavík and the University of Iceland. The library is written in Java and sports a variety of NLP tools, including:

- Tokenization
- Part-of-speech tagging
- Named entity recognition
- Parsing
- Lemmatization
- Morphological analysis

Although today considered a legacy application and well outside the realm of state of the art technology, IceNLP is still maintained and has both practical and educational value. With this in mind, a simple way to implement the library in Python was developed, which is the basis for this Python package.

## Prerequisites

This package runs on Python 3.8 or newer. Furthermore, as the package uses unmodified IceNLP source code, you will need to have Java installed on your system. For further information, see the [IceNLP documentation](https://github.com/hrafnl/icenlp/blob/master/core/doc/IceNLP.tex).

## Installation

```bash
pip install icenlpy
```

To edit the source code, clone the repository and install the package in editable mode:

```bash
git clone https://github.com/hinrikur/IceNLPy
cd IceNLPy
# [ Activate your virtualenv here if you have one ]
pip install -e .
```

## Acknowledgements

IceNLP is developed and maintained by Hrafn Loftsson and the University of Reykjavík. The IceNLPy Python wrapper was developed by Hinrik Hafsteinsson.
