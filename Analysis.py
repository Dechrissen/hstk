import sqlite3
from time import sleep


def searchSnaps(phrase):
    """Searches through snaps in the Headline Snap database for matches on the given string PHRASE.

    args
        phrase : string to be searched from -s args option

    returns
        null
    """
    if phrase != None:
        print("Searching Headline Snap database ...")
        sleep(2)
        search_output = '\nNO RESULTS\n'
        db_file = r"./data/db/hs.db"
        # connect to the database
        try:
            con = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)
            return
        cur = con.cursor()
        # text search
        phrase_binding = "%" + phrase + "%" # sqlite formatting for binding below
        res = cur.execute('''SELECT * FROM headlines WHERE text LIKE (?)''', (phrase_binding,))
        matches = res.fetchall()
        if len(matches) == 0:
            print(search_output)
            return
        search_cap = 10
        search_output = '\n'
        for match in matches[:search_cap]:
            search_output = search_output + match[0] + '\n'
        print(search_output)
        return
    else:
        return

def getTotalSnaps(total=False):
    """Prints the total number of Headline Snaps in the database.

    args
        total : boolean value from -t args option

    returns
        null
    """
    if total:
        print("Fetching total Headline Snap count ...")
        sleep(2)
        db_file = r"./data/db/hs.db"
        # connect to the database
        try:
            con = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)
            return
        cur = con.cursor()
        # select every row in headlines table
        res = cur.execute("SELECT Count(*) FROM headlines")
        print("Total:", res.fetchone()[0])
        con.close()
        return
    else:
        return

def getRandomSnap(number):
    """Prints NUMBER random Headline Snaps from the database.

    args
        number : int value from -r args option

    returns
        null
    """
    if number != None:
        print("Fetching", number, "random {} ...".format("Headline Snap" if number == 1 else "Headline Snaps"))
        sleep(2)
        db_file = r"./data/db/hs.db"
        # connect to the database
        try:
            con = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)
            return
        cur = con.cursor()
        # select a random number of snaps from the database equal to the value of `number`
        res = cur.execute('''SELECT * FROM headlines ORDER BY RANDOM() LIMIT ?''', (number,))

        print(res.fetchall()[:number])
        con.close()
        return
    else:
        return
    