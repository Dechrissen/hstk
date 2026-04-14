from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from time import sleep
import re


def generateWordCloud():
    '''Generates a word cloud based on a text corpus created from the Headline Snap database.
    
    args
        null

    returns
        null
    '''
    print("Generating word cloud of most common words in the database ...")
    # download these necessary things
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')

    # define stop words for using later
    stop_words = set(stopwords.words('english'))

    # instantiate lemmatizer
    wl = WordNetLemmatizer()
    
    corpus = ''
    with open("./data/corpus.txt", "r", encoding='utf-8') as f:
        corpus = f.readlines()

    text_data = ''
    for line in corpus:
        text_data += line.strip('\n') + " "

    text_data = text_data.split()
    text_data = [w.lower() for w in text_data if not w.lower() in stop_words]

    # lemmatize
    text_data = [wl.lemmatize(word) for word in text_data if word not in stop_words]

    # join
    text_data = " ".join(text_data)

    # remove multi-word garbage phrases
    garbage_phrases = [
        "daughter s",
        "u government",
    ]

    for phrase in garbage_phrases:
        text_data = text_data.replace(phrase, "")

    # remove standalone words "u" and "s"
    # use regex to avoid removing them inside other words
    text_data = re.sub(r"\b(u|s)\b", "", text_data)

    # instantiate wordcloud object
    cloud = WordCloud(width=4800,
                    height=4800,
                    max_words=100,
                    colormap='Pastel2',).generate_from_text(text_data)
    print(len(cloud.words_))

    # define figure options and show it
    plt.figure(figsize=(8,8))
    plt.imshow(cloud)
    plt.axis('off')


    #plt.title("Headline Snaps - Common Words", fontsize=16)
    print("Done.")
    sleep(1)
    print('Displaying word cloud ...')

    plt.savefig("wordcloud.png", dpi=600, bbox_inches='tight', pad_inches=0.3, facecolor='black')

    plt.show()
    return