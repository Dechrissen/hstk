import sqlite3

def getTotalSnaps(total=False):
    """Prints the total number of Headline Snaps in the database.

    args
        total : boolean value from -t args option

    returns
        null
    """
    if total:
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
    