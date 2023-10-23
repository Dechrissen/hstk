from Functions import *
import os

# create the data directory if it doesn't exist
path_to_data = './data'
print("Checking for directory 'data' ...")
if not os.path.exists(path_to_data):
    print("Directory 'data' being created ...")
    os.makedirs(path_to_data)
    print('Done.')
else:
    print("Directory 'data' already exists")

image_directory = './data/snaps/'

# test for converting a directory of snaps (images) to strings
#convertDirectory(image_directory)

# test for creating sqlite db
db_file_path = r"./data/db/hs.db"
createDatabase(db_file_path)
addToDatabase(db_file_path)
