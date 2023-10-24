from Functions import *
import os

initialize()

# test for converting a directory of snaps (images) to strings
convertDirectory('./data/src/raw')

# test for creating sqlite db
#db_file_path = r"./data/db/hs.db"
#addToDatabase(db_file_path)
