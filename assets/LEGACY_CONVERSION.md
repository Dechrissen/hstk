## Converting legacy or non-compliant Headline Snaps

In some cases, you might need to use [a9t9](https://github.com/A9T9/Free-OCR-Software), a free and open source OCR GUI application for Windows, for OCRing some legacy Headline Snap image files, i.e., those which do not follow the [guidelines](./GUIDELINES.md) (background not black, text too high in the frame, etc.). This software is (for some reason) more capable of OCRing these non-compliant images than our Tesseract-based pipeline.

### Instructions

(Windows) Prepare a folder of the all the non-compliant Headline Snaps you need to convert to text. Open a9t9 (example below), click "Open Images", and navigate to your folder. Select all images in the folder. After a9t9 is finished loading the images in, tick the box "Process All Documents", then click "Start Ocr". After the process is complete, you will see all OCRed images on the right side of the window. Click "Save as Text" and save the file to `/hstk/scripts`, naming it `a9t9.txt` (filename is important).

<p align="center"><img src="./a9t9.png" alt="a9t9 example" style="width: 60%;" /></p>

Add to the terms define in the `filters` list in `/config.json`, so that terms that might show up in your images get properly filtered out by the script.

`cd` to the `/scripts` directory.

Now, invoke the script `clean-a9t9.py` by running:

```
python clean-a9t9.py
```

The cleaned file will be output to `/data/src/text/a9t9_cleaned.txt`. It's recommended to review the sentences in the output file; there could still be some weird artifacts in the text if the background was not completely black.

Then, to add the contents of all the `.txt` files in `/data/src/text` to the database, run:

```
python hstk.py -a
```
