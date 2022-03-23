# This script takes an a9t9 output file 'a9t9.txt' and converts it into a cleaned
# file 'cleaned.txt' (e.g. no Snapchat-specific text, no stray newlines, etc.),
# with one headline snap per line.

# read in a9t9 output as a full string
with open("a9t9.txt", "r") as f:
    raw_content = f.read()

# define filters to remove from the string
filters = ['Send a chat \n', 'CHAT \n', 'Derek Andersen \n', 'Evan Martin \n']
x = raw_content

# replace instances of 'Send a chat', etc. with empty string
for filter in filters:
    x = raw_content.replace(filter, '')

# split into a list at newline characters
lines = x.split('\n')

# start a counter to get list indeces
c = 0
for line in lines:
    # replace the a9t9 separator with a pipe
    if '===' in line:
        lines[c] = '|'
    c += 1

# join this back into a string (at this point there are no newline characters)
x = "".join(lines)
x = x.split(' |')

# write each line to a file 'cleaned.txt'
# one headline snap per line
with open("cleaned.txt", "w") as f:
    for line in x:
        f.write(line + '\n')
