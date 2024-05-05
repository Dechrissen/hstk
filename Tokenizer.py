from Functions import *
from time import sleep

def updateTokens(token_db_path):
    '''Updates all of the tokens and their counts based on the latest dump of the corpus.
    
    args
        token_db_path : the path to the token database file
    
    returns
        null
    '''    
    # first delete the token db so we can start fresh
    con = None
    try:
        con = sqlite3.connect(token_db_path)
    except sqlite3.Error as e:
        print(e)
        return

    cur = con.cursor()
    cur.execute("""DROP TABLE tokens""")
    con.close()

    # recreate an empty token db
    createTokenDatabase(token_db_path)

    print("Updating token database with counts ...")
    sleep(1)

    # then iterate over every snap in the corpus and tokenize them and add them to the token db
    with open("./data/corpus.txt", "r", encoding="utf-8") as corpus_file:
        corpus = corpus_file.read().splitlines()
        for snap in corpus:
            cleaned_snap = cleanText(snap)
            tokenized_snap = tokenizeSnap(cleaned_snap)
            # iterate over the tokenized snap (a dictionary) keys and add all the tokens/counts to the token db
            for key in tokenized_snap.keys():
                token = key
                count = tokenized_snap[key]
                addToTokenDatabase(token_db_path, token, count)

    print("Done.")
    return
    
                

def tokenizeSnap(snap):
    '''Extracts unique tokens from a Headline Snap and assigns counts to each.

    args
        snap : a Headline Snap to be tokenized

    returns
        tokenized_snap : a dictionary of token:count (string:int) key/value pairs
    '''

    # split snap (string) into list of tokens
    snap_as_list = snap.split()
    for index in range(len(snap_as_list)):
        snap_as_list[index] = cleanText(snap_as_list[index])

    tokenized_snap = {}

    # add each token and its count to tokenized_snap
    for token in snap_as_list:
        tokenized_snap[token] = tokenized_snap.get(token, 0) + 1

    return tokenized_snap
        

def getTokenCount(token_db_path, token):
    '''Returns the frequency count for some token in the token database.
    
    args
        token_db_path : the path to the token database file
        token : the token whose count should be returned

    returns
        count (int)
    '''
    con = None
    count = 0
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
    # if it doesn't exist, return 0
    if exists.fetchone()[0] == 0:
        # count is already initialized to 0, so do nothing
        pass
    # if it does exist, return the count of the token
    else:
        # get rowid of token
        res = cur.execute('''SELECT rowid FROM tokens WHERE token = (?)''', (token,))
        rowid = res.fetchone()[0]
        # increment count using row id
        res = cur.execute('''SELECT count FROM tokens WHERE rowid = (?)''', (rowid,))
        x = res.fetchone()[0]
        count = x

    # commit the transaction on the connection object
    con.commit()

    con.close()
    return count