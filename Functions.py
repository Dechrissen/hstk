import pytesseract
import os
from PIL import Image, ImageOps, ImageEnhance
import sqlite3
import platform


def initialize():
    """Initializes the project for use: creates local directories, creates 
    empty db file.

    args
        null

    returns
        null
    """
    print("Performing first-time setup ...")

    # create the local directories (which should not exist on remote)
    dirs = ['./data/db', './data/src/raw', './data/src/text']
    for dir in dirs:
        createDirectory(dir)

    db_file = r"./data/db/hs.db"
    createDatabase(db_file)

    print("Setup complete.")
    return

def tweakImage(image_file):
    """Crops (removes top and bottom portions) and inverts contrast (into black
    text on white background) for a raw Headline Snap image.

    args
        image_file : the path to an image file

    returns
        cropped_image : a PIL Image object
    """

    image = Image.open(image_file)

    # remove the 'A' channel if the image has one
    if image.mode == 'RGBA':
        r,g,b,a = image.split()
        image = Image.merge('RGB', (r,g,b))

    # invert the contrast
    image = ImageOps.invert(image)
    contrast = ImageEnhance.Contrast(image)
    image = contrast.enhance(2)

    # get the dimensions of the image
    width, height = image.size

    # set the amount of top & bottom to trim off (20% here)
    trim = .2 * height

    # crop the image
    crop_region = (0, trim, width, (height - trim))
    cropped_image = image.crop(crop_region)

    # show the image for testing purposes
    #cropped_image.show()

    return cropped_image

def imageToText(tweaked_image):
    """Converts a tweaked Headline Snap image into text.

    args
        tweaked_image : a cropped and contrast-inverted Headline Snap

    returns
        cleaned_text : the Headline Snap as a string
    """
    # tesseract needs to be present in your PATH (both Windows and Linux)
    # check current platform
    if platform.system() == 'Linux':
        pass
    elif platform.system() == 'Windows':
        # Windows only: set the location of the tesseract executable
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    else:
        print("Your operating system is not supported.")
        quit()
    # set the config for the conversion (not sure what this does)
    config = ("--psm 6")

    # OCR
    text = pytesseract.image_to_string(tweaked_image, config=config, lang='eng')

    # clean the raw text from the OCR
    cleaned_text = text.replace('\n', ' ')

    return cleaned_text

def convertDirectory(dir):
    """Iterates over a directory of images (Headline Snaps) and runs them through
    the crop & text conversion functions. The resulting converted headline
    snaps will be appended to a text file 'output.txt', one per line.

    args
        dir : the directory containing the images to be converted

    returns
        null
    """

    print("Converting Headline Snaps...")

    # intermediate list to store converted images before they're written to file
    converted_snaps = []

    # a count for progress output in console
    count = 0

    # loop over the raw images, running them through our conversion functions
    for filename in os.listdir(dir):
        # convert each image into text
        file = os.path.join(dir, filename)
        tweaked_image = tweakImage(file)
        text = imageToText(tweaked_image)
        # add image (as text) to intermediate list converted_snaps
        converted_snaps.append(text + '\n')
        # progress output
        count += 1
        print('Converted ' + str(count))

    print('Done.')
    print('Successfully converted', str(count), 'Headline Snaps into text.')
    print('Creating output file...')

    # write Headline Snaps stored in intermediate list to final output file
    with open('./data/src/text/output.txt', 'w', encoding='utf-8') as output_file:
        output_file.writelines(converted_snaps)

    print('Done.')
    print('Output is available at /data/src/text/output.txt.')
    return

def createDatabase(db_file_path):
    """Creates an sqlite database file for Headline Snaps, with all necessary columns.

    args
        db_file_path : the path where the sqlite database file will exist

    returns
        null
    """

    con = None
    try:
        con = sqlite3.connect(db_file_path)
    except sqlite3.Error as e:
        print(e)
        return

    cur = con.cursor()
    try:
        # this UNIQUE declaration lets us use the IGNORE keyword when adding to the database, to avoid duplicates 
        cur.execute('''CREATE TABLE headlines(
                            text,
                            UNIQUE(text))''')
    except sqlite3.Error as e:
        print(e)
        return

    con.close()
    print("Empty database created.")
    return

def addToDatabase(db_file, text_file):
    """Adds Headline Snaps from a text file into the database.

    args
        db_file : the path to the database
        text_file : the file containing lines of Headline Snaps as text

    returns
        null
    """
    # connect to the database
    try:
        con = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
        return

    cur = con.cursor()

    # open the text file with Headline Snaps
    with open(text_file, mode='r', encoding='utf-8') as file:
        for snap in file:
            snap = snap.split('\n')[0]
            # add snap to the table (note the comma after snap to make it a tuple)
            cur.execute('''INSERT OR IGNORE INTO headlines(text)
                           VALUES(?)''', (snap,))

    # commit the transaction on the connection object
    con.commit()

    # test that the values were added to the table
    res = cur.execute("SELECT text FROM headlines")
    print(res.fetchall())

    con.close()
    return

def createDirectory(path):
    """Creates a directory.

    args
        path : the path where the directory should exist

    returns
        null
    """
    if not os.path.exists(path):
        print("Directory '{0}' being created ...".format(os.path.basename(path)))
        os.makedirs(path)
        print('OK')
        return
    else:
        return
