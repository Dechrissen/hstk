from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
#print(stopwords.words('english'))

stop_words = set(stopwords.words('english'))
 

corpus = ''
with open("./data/corpus.txt") as f:
    corpus = f.readlines()

text_data = ''
for line in corpus:
    text_data += line.strip('\n') + " "

text_data = text_data.split()
#print(text_data)
#raise SystemExit(1)


#print(text_data)
#raise SystemExit(1)

text_data = [w.lower() for w in text_data if not w.lower() in stop_words]

wl = WordNetLemmatizer()
text_data = [wl.lemmatize(word) for word in text_data if not word in stop_words]

#print(text_data)
#raise SystemExit(1)

text_data = ' '.join(text_data)


#print(text_data)

#Instantiate wordcloud object and use method to feed it our corpus
wc = WordCloud(width=400,
                height=330,
                max_words=150,
                colormap='tab20c',).generate_from_text(text_data)

#Use matplotlib.pyplot to display the fitted wordcloud
#Turn axis off to get rid of axis numbers
plt.figure(figsize=(10,8))
plt.imshow(wc)
plt.axis('off')
plt.title("Headline Snaps", fontsize=14)
plt.show()