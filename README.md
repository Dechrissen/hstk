# hstk – Headline Snap Toolkit

`hstk` provides a collection of tools for creating a database of [Headline Snaps](./assets/WHAT.md) and interfacing with the database. Some of its built-in tools for data analysis include language modeling and data visualization functions. It can also synthesize new language data based on a trigram model.

## Table of Contents

- [Initial setup](#initial-setup)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Converting non-compliant Headline Snaps](#converting-non-compliant-headline-snaps)


## Initial setup

First, clone this repository (or fork your own copy, then clone that).

```
git clone git@github.com:Dechrissen/hstk.git
```

## Prerequisites

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


## Usage

`cd` to the project directory.

To get a detailed help message, run:

```
python hstk.py -h
```

### On data persistence

When you run this software for the first time, a directory called `/data` will be created locally within the project directory. This is where you will place your own source image data (in `/data/src/raw`), and where various generated data will be output by the software.

The idea is that the data directory (or at least, the database files that get created in `/data/db`) should persist regardless of whatever subcommands you run with `hstk`. The source data you provide can theoretically stay in the data directory forever, and new data can be added at any time. Updates to this software, for example, shouldn't affect existing data in your local directory.

The source data is what's used to generate the entries in the database files (e.g. `/data/db/hs.db`). Whenever new source data is added to `/data/src/raw`, running the conversion command (`python hstk.py -c`) will update the database.

Similarly, newline-separated files containing Headline Snaps as text can be added to `/data/src/text` at any time, with a `.txt` extension. Then `python hstk.py -a` will add those to the database.

### More usage examples



## Converting non-compliant Headline Snaps

In some cases, you might need to use [a9t9](https://github.com/A9T9/Free-OCR-Software) to convert some legacy Headline Snap image files, i.e., those which do not follow the [guidelines](./assets/GUIDELINES.md) (background not black, text too high in the frame, etc.). For detailed instructions, see [this guide](./assets/LEGACY_CONVERSION.md).



