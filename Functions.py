import pytesseract
import os
from PIL import Image, ImageOps, ImageEnhance
import sqlite3
import platform
import json
from time import sleep


def initialize(hs_db_path, token_db_path):
    """Initializes the project for use: creates local directories, creates 
    empty db files.

    args
        hs_db_path : the path to the headline snap database
        token_db_path : the path to the token database

    returns
        null
    """
    # try to open cache.json (if it exists)
    try:
        with open("cache.json", "r") as jsonFile:
            cache = json.load(jsonFile)
    except FileNotFoundError:
        # create cache file if it doesn't exist, initialize to false
        data = json.loads("""{"initialized":false}""")
        with open("cache.json", "rw") as jsonFile:
            json.dump(data, jsonFile)
            cache = json.load(jsonFile)
        print("Cache file created.")

    
    # check if initialize has been run successfully already
    # if yes, return
    if cache["initialized"]:
        return

    # if no, run all the initialize steps
    print("Performing first-time setup ...")
    sleep(1)

    # create config file, filled in with filters for clean-a9t9.py
    with open("config.json", "w") as jsonFile:
        data = json.loads("""{"filters":["Send a chat", "CHAT"]}""")
        json.dump(data, jsonFile)
    print("Config file created.")

    # create the local directories (which should not exist on remote)
    dirs = ['./data/db', './data/src/raw', './data/src/text']
    for dir in dirs:
        createDirectory(dir)

    # create the database files
    createSnapDatabase(hs_db_path)
    createTokenDatabase(token_db_path)

    # set cache so initialize doesn't run anymore
    cache["initialized"] = True
    with open("cache.json", "w") as jsonFile:
        json.dump(cache, jsonFile)

    sleep(1)
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
    the crop & text conversion functions. The resulting converted Headline
    Snaps will be appended to a text file 'ocr_output.txt', one per line.

    args
        dir : the directory containing the images to be converted

    returns
        null
    """

    print("Converting Headline Snaps ...")

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
    sleep(1)
    print('Successfully converted', str(count), 'Headline Snap image files to text.')
    print('Creating output file ...')
    sleep(1)

    # write Headline Snaps stored in intermediate list to final output file
    with open('./data/src/text/ocr_output.txt', 'w', encoding='utf-8') as output_file:
        output_file.writelines(converted_snaps)

    print('Done.')
    sleep(1)
    print('Output is available at /data/src/text/ocr_output.txt')
    return

def createSnapDatabase(db_file_path):
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
    
    # commit the transaction on the connection object
    con.commit()
    con.close()
    print("Empty Headline Snap database created.")
    return

def addToSnapDatabase(db_file, src_text_dir):
    """Adds Headline Snaps from a text file into the database.

    args
        db_file : the path to the database
        src_text_dir : the file containing lines of Headline Snaps as text

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

    print("Adding Headline Snaps from files in " + str(src_text_dir) + " to the database ...")
    sleep(1)

    # open all text files in /data/src/text
    for file in os.listdir(src_text_dir):
        if file.endswith(".txt"):
            with open(os.path.join(src_text_dir,file), mode='r', encoding='utf-8') as f:
                for snap in f:
                    snap = snap.split('\n')[0]
                    # add snap to the table (note the comma after snap to make it a tuple)
                    cur.execute('''INSERT OR IGNORE INTO headlines(text)
                                VALUES(?)''', (snap,))

    # commit the transaction on the connection object
    con.commit()

    # DEBUG
    # test that the values were added to the table
    #res = cur.execute("SELECT text FROM headlines")
    #print(res.fetchall())

    con.close()
    print("Done.")
    return

def createTokenDatabase(db_file_path):
    """Creates an sqlite database file for individual token counts, with all necessary columns.

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
        # the PRIMARY KEY option ... TODO
        cur.execute('''CREATE TABLE tokens(
                            token TEXT PRIMARY KEY,
                            count INTEGER,
                            UNIQUE(token))''')
    except sqlite3.Error as e:
        print(e)
        return

    # commit the transaction on the connection object
    con.commit()
    con.close()
    print("Empty token database created.")
    return

def addToTokenDatabase(token_db_path, token, increment):
    """Adds tokens to the token database and/or updates a token's count.

    args
        token_db_path : the path to the database
        token : the token to be added to the database
        increment : the amount to increment a token's count by (1 means it's new)

    returns
        null
    """
    # connect to the database
    try:
        con = sqlite3.connect(token_db_path)
    except sqlite3.Error as e:
        print(e)
        return

    cur = con.cursor()

    # first check if the token is already in the db
    # this returns 1 if it exists in the db, and 0 if not (in a tuple)
    exists = cur.execute('''SELECT EXISTS( SELECT 1 FROM tokens WHERE token = (?) )''', (token,))
    # if it doesn't exist, add token with initial count of 1
    if exists.fetchone()[0] == 0:
        cur.execute('''INSERT OR IGNORE INTO tokens(token,count)
                           VALUES(?,?)''', (token,increment))
    # if it does exist, increment its count by 1
    else:
        # get rowid of token
        res = cur.execute('''SELECT rowid FROM tokens WHERE token = (?)''', (token,))
        rowid = res.fetchone()[0]
        # increment count using row id
        cur.execute('''UPDATE tokens SET count = count + (?) WHERE rowid = (?)''', (increment,rowid))

    # commit the transaction on the connection object
    con.commit()

    # DEBUG
    # test that the values were added to the table
    #res = cur.execute("SELECT * FROM tokens")
    #print(res.fetchall())

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

def isOddSnap(snap):
    '''Checks whether a given snap contains symbols that suggest it doesn't follow 
    news headline format, and thus should be filtered out from the corpus that will 
    be used for model training.
    
    args
        snap : the snap to be checked for odd symbols

    returns
        bool
    '''
    oddities = ['(', ')', '!']
    for symbol in oddities:
        if symbol in snap:
            return True
    return False

def cleanText(text):
    '''Cleans a string, removing punctuation and making lower case.
    Preserves phrasal (hyphenated) adjectives and apostrophes.

    args
        text : the string to clean

    returns
        text : the cleaned string
    '''
    text = text.lower()
    # define filters to remove from the string
    filters = [',', '.', ')', '(', '[', ']', '{', '}', '<', '>', '!', '?', ';', ':', '"']

    # replace instances of filters with empty string
    for filter in filters:
        text = text.replace(filter, '')

    return text

def dumpCorpus(hs_db_path):
    '''Dumps all Headline Snaps in the database to a text file after running them
    through the cleanText() function. For use with language model training functions.
    
    args
        hs_db_path : the path to the headline snap database

    returns
        null
    '''
    all_cleaned_snaps = []
    
    # connect to the database
    try:
        con = sqlite3.connect(hs_db_path)
    except sqlite3.Error as e:
        print(e)
        return
    cur = con.cursor()
    # select text column from headlines table
    res = cur.execute('''SELECT text FROM headlines''')

    for snap in res.fetchall():
        # clean snaps from fetchall output
        snap = snap[0].strip(' ') + '\n'
        # check if the snap is 'odd', and thus shouldn't be in the corpus for training
        if not isOddSnap(snap):
            # if not, append cleaned snap to all_cleaned_snaps list
            all_cleaned_snaps.append(snap)
    
    # write all snaps from all_cleaned_snaps to corpus.txt
    with open('./data/corpus.txt', 'w', encoding='utf-8') as dump_file:
        dump_file.writelines(all_cleaned_snaps)

    # commit the transaction on the connection object
    con.commit()
    con.close()
    return

def dumpAll(hs_db_path):
    '''Dumps all Headline Snaps in the database to a text file.

    args
        hs_db_path : the path to the headline snap database

    returns
        null
    '''
    # initialize empty list to store all db snaps
    all_snaps = []

    # connect to the database
    try:
        con = sqlite3.connect(hs_db_path)
    except sqlite3.Error as e:
        print(e)
        return
    cur = con.cursor()
    # select text column from headlines table
    res = cur.execute('''SELECT text FROM headlines''')

    print("Gathering all Headline Snaps to be exported ...")
    sleep(1)
    for snap in res.fetchall():
        # clean snaps from fetchall output
        snap = snap[0].strip(' ') + '\n'
        # append all snaps to all_snaps list
        all_snaps.append(snap)

    # write all snaps from all_snaps to dump.txt
    print("Dumping all Headline Snaps to a text file ...")
    sleep(1)
    with open('./data/dump.txt', 'w', encoding='utf-8') as dump_file:
        dump_file.writelines(all_snaps)

    print('Done.')
    sleep(1)
    print('Output is available at /data/dump.txt')
    # commit the transaction on the connection object
    con.commit()
    con.close()
    return

def deleteDatabases(hsdb_path,token_db_path):
    '''Deletes and recreates both the Headline Snap and token database files.
    
    args
        hsdb_path : path to the headline snap database file
        token_db_path : path to the token database file
    
    returns
        null
    '''
    # delete headline snap db
    con = None
    try:
        con = sqlite3.connect(hsdb_path)
    except sqlite3.Error as e:
        print(e)
        return

    cur = con.cursor()
    cur.execute("""DROP TABLE headlines""")
    # commit the transaction on the connection object
    con.commit()
    con.close()
    print("Headline Snap database file cleared.")

    # recreate an empty headline snap db
    createSnapDatabase(hsdb_path)

    # delete token db
    con = None
    try:
        con = sqlite3.connect(token_db_path)
    except sqlite3.Error as e:
        print(e)
        return

    cur = con.cursor()
    cur.execute("""DROP TABLE tokens""")
    # commit the transaction on the connection object
    con.commit()
    con.close()
    print("Token database file cleared.")

    # recreate an empty token db
    createTokenDatabase(token_db_path)

    return
    