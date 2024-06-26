import sqlite3
from time import sleep


def searchSnaps(hs_db_path, phrase):
    """Searches through snaps in the Headline Snap database for matches on the given string.

    args
        hs_db_path : the path to the headline snap database
        phrase : string to be searched from -s args option

    returns
        null
    """
    if phrase != None:
        print("Searching Headline Snap database ...")
        sleep(1)
        search_output = '\nNO RESULTS\n'

        # connect to the database
        try:
            con = sqlite3.connect(hs_db_path)
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
        
        # commit the transaction on the connection object
        con.commit()
        con.close()

        # max amount of matches
        search_cap = 20
        # initialize a count for printing numbers before each snap
        count = 1
        search_output = '\n'
        for match in matches[:search_cap]:
            # append each match to search_output
            search_output = search_output + '\t' + str(count) + ') ' + match[0] + '\n'
            count += 1
        print(search_output)
        return
    else:
        return

def getTotalSnaps(hs_db_path, total=False):
    """Prints the total number of Headline Snaps in the database.

    args
        hs_db_path : the path to the headline snap database
        total : boolean value from -t args option

    returns
        null
    """
    if total:
        print("Fetching total Headline Snap count ...")
        sleep(1)
        
        # connect to the database
        try:
            con = sqlite3.connect(hs_db_path)
        except sqlite3.Error as e:
            print(e)
            return
        cur = con.cursor()
        # select every row in headlines table
        res = cur.execute("SELECT Count(*) FROM headlines")
        print("\nTotal:", res.fetchone()[0])
        # commit the transaction on the connection object
        con.commit()
        con.close()
        return
    else:
        return

def getRandomSnap(hs_db_path, number):
    """Prints NUMBER random Headline Snaps from the database.

    args
        hs_db_path : the path to the headline snap database
        number : int value from -r args option

    returns
        null
    """
    if number != None:
        print("Fetching", number, "random {} ...\n".format("Headline Snap" if number == 1 else "Headline Snaps"))
        sleep(1)

        # connect to the database
        try:
            con = sqlite3.connect(hs_db_path)
        except sqlite3.Error as e:
            print(e)
            return
        cur = con.cursor()
        # select a random number of snaps from the database equal to the value of `number`
        res = cur.execute('''SELECT * FROM headlines ORDER BY RANDOM() LIMIT ?''', (number,))

        # initialize a count for printing numbers before each snap
        count = 1
        for snap in res.fetchall()[:number]:
            # clean up snap from res.fetchall() output
            snap = snap[0].strip(' ')
            print('\t' + str(count) + ') ' + snap)
            count += 1

        con.close()
        return
    else:
        return
    