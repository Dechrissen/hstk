# hstk – Headline Snap Toolkit

`hstk` provides a collection of tools for creating a database of [Headline Snaps?](./assets/WHAT.md) and interfacing with the database. Some of its built-in tools for data analysis include language modeling and data visualization functions. It can also synthesize new language data based on a trigram model.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Converting non-compliant Headline Snaps](#using-a9t9-to-convert-legacy-or-non-compliant-headline-snaps)

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

TODO provide more example usage

## Converting non-compliant Headline Snaps

In some cases, you might need to use [a9t9](https://github.com/A9T9/Free-OCR-Software) to convert some legacy Headline Snap image files, i.e., those which do not follow the [guidelines](./assets/GUIDELINES.md) (background not black, text too high in the frame, etc.). For detailed instructions, see [this guide](./assets/LEGACY_CONVERSION.md).



