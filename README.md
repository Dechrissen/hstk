# hstk – Headline Snap Toolkit

`hstk` provides a collection of tools for creating a database of fabricated news headlines ([Headline Snaps](./assets/WHAT.md)) and interfacing with the database. Some of its built-in tools include language modeling, data analysis, data visualization tools. It can also synthesize new language data (news headlines) based on a trigram model.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Usage and features](#usage)
- [Converting non-compliant Headline Snaps](#converting-non-compliant-headline-snaps)


## Installation

First, clone this repository (or fork your own copy, then clone that).

```
git clone git@github.com:Dechrissen/hstk.git
```

Alternatively, you can download the latest release's source code from the [releases](https://github.com/Dechrissen/hstk/releases) section of this repository. In that case, you'd need to extract it.

## Setup

Ensure you have Python 3 installed.

`cd` to the project directory.

To install dependencies, run:

```
pip install -r requirements.txt
```

(For this to work on Windows, you might need to prefix the command with `python -m`, i.e. `python -m pip install -r requirements.txt`).

### Installing the Tesseract executable

The Tesseract executable (engine) is required for the OCR backend in this toolkit. It is available on both Windows and Linux.

- [Windows installer](https://github.com/UB-Mannheim/tesseract/wiki)
    - make sure you install the executable in this location exactly: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- [Linux instructions](https://tesseract-ocr.github.io/tessdoc/Installation.html)
    - no special location instructions; just install via your distro's package manager

To perform the first-time setup, run:
```
python hstk.py
```
without any arguments. This will initialize the data directories for use.


## Usage

`cd` to the project directory.

To get a detailed help message, run:

```
python hstk.py -h
```

### On data persistence

When you run this toolkit for the first time, a directory called `/data` will be created locally within the project directory. This is where you will place your own source image data (in `/data/src/raw`), and where various generated data will be output by the tools.

The idea is that the data directory (or at least, the database files that get created in `/data/db`) should persist regardless of whatever subcommands you run with `hstk`. The source data you provide can theoretically stay in the data directory forever, and new data can be added at any time. Updates to this toolkit, for example, shouldn't affect existing data in your local directory.

The source data is what's used to generate the entries in the database files (e.g. `/data/db/hs.db`). Whenever new source data is added to `/data/src/raw`, running the conversion command (`python hstk.py -c`) will update the database.

Similarly, newline-separated files containing Headline Snaps as text can be added to `/data/src/text` at any time, with a `.txt` extension. Then `python hstk.py -a` will add those to the database.

### Using the included sample dataset

A sample dataset of 24 image files is included in the repository. By default, they will not be used. To include them in your database, simply copy them from `/sample` to `/data/src/raw` (after running the initial setup command):
```
cp sample/* /data/src/raw/
```
Then, to convert all of these images and add them to your database, run:
```
python hstk.py --convert
```

### Features

There are several commands at your disposal in this toolkit.

command | flag | description
--- | --- | ---
add | `-a` | adds the current contents of the files in `/data/src/text` (newline-separated) to the database
total | `-t` | output the total number of Headline Snaps in the database
random | `-r` | print a random Headline Snap from the database
convert | `-c` | convert the Headline Snap image files in `/data/src/raw` to text via OCR and output them to `/data/text/ocr_output.txt`, then adds all contents of the `/data/text` directory to the database
export | `-x` | dump all Headline Snaps from the database to a text file at `/data/dump.txt`
search | `-s` | query the database for Headline Snaps containing a provided search phrase
delete | `-d` | delete all data from the Headline Snap and token databases

Note: run the toolkit with the `-h` flag to see all commands.

Additional functionality exists via **subcommands**, outlined below.

#### Via the `tokenizer` subcommand ...
command | flag | description
--- | --- | ---
update_tokens | `-u` | iterate through all Headline Snaps in the database and add all unique tokens to a separate token database, keeping track of counts
query_tokens | `-q` | print the number of times some individual token appears in the database, according to the token database

#### Via the `trigrams` subcommand ...
command | flag | description
--- | --- | ---
generate | `-g` | train a trigram language model on the database and synthesize a new Headline Snap based on it

#### Via the `visualizer` subcommand ...
command | flag | description
--- | --- | ---
word_cloud | `-w` | generate a word cloud representing the most commonly occurring terms in the database

For detailed help with each subcommand, run:

```
python htsk.py <SUBCOMMAND> -h
```

## Converting non-compliant Headline Snaps

In some cases, you might need to use [a9t9](https://github.com/A9T9/Free-OCR-Software) to convert some legacy Headline Snap image files, i.e., those which do not follow the [guidelines](./assets/GUIDELINES.md) (background not black, text too high in the frame, etc.). For detailed instructions, see [this guide](./assets/LEGACY_CONVERSION.md).



