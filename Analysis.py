# File which will contain all the functions pertaining to analyzing data from the constructed database, tagging, tokenizer function, etc.
import sqlite3

def getTotalSnaps(total=False):
    if total:
        db_file = r"./data/db/hs.db"
        # connect to the database
        try:
            con = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)
            return
        cur = con.cursor()
        res = cur.execute("SELECT Count(*) FROM headlines")
        print(res.fetchone()[0])
        con.close()
        return
    else:
        return
