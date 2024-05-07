from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from time import sleep


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
    text_data = [wl.lemmatize(word) for word in text_data if not word in stop_words]

    text_data = ' '.join(text_data)

    # instantiate wordcloud object
    cloud = WordCloud(width=400,
                    height=330,
                    max_words=150,
                    colormap='tab20c',).generate_from_text(text_data)

    # define figure options and show it
    plt.figure(figsize=(10,8))
    plt.imshow(cloud)
    plt.axis('off')
    plt.title("Headline Snaps - Common Words", fontsize=16)
    print("Done.")
    sleep(1)
    print('Displaying word cloud ...')
    plt.show()
    return