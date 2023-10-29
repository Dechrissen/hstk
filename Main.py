from Functions import *
import os

initialize()

# test for converting a directory of snaps (images) to strings
#convertDirectory('./data/src/raw')

# test for creating sqlite db
db_file = r"./data/db/hs.db"
text_file = r"./data/src/text/hs_derek.txt"
createDatabase(db_file)
addToDatabase(db_file, text_file)
