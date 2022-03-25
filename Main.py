from Functions import *

file = './data/test.png'

tweaked_image = tweakImage(file)
text = imageToText(tweaked_image)
print(text)
