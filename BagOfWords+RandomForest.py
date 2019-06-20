import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
import pydot

def decontracted(phrase):   #Dictionary for expanding contractions
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    phrase = re.sub(r"won\’t", "will not", phrase)
    phrase = re.sub(r"can\’t", "can not", phrase)

    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)

    phrase = re.sub(r"n\’t", " not", phrase)
    phrase = re.sub(r"\’re", " are", phrase)
    phrase = re.sub(r"\’s", " is", phrase)
    phrase = re.sub(r"\’d", " would", phrase)
    phrase = re.sub(r"\’ll", " will", phrase)
    phrase = re.sub(r"\’t", " not", phrase)
    phrase = re.sub(r"\’ve", " have", phrase)
    phrase = re.sub(r"\’m", " am", phrase)
    return phrase


train = pd.read_csv("inputs/UseCase4TrainShuffled.csv", keep_default_na=False, header=0, delimiter='\t', quoting=3)
test = pd.read_csv("inputs/UseCase4TestShuffled.csv", keep_default_na=False, header=0, delimiter='\t', quoting=3)
#Reads CSV file


def article_cleanup(raw_article):
    #General function to take in CSV file and clean it up for vectorization
    text = BeautifulSoup(raw_article, features="html.parser").get_text
    letters_only = re.sub('/[^\w\']+|\'(?!\w)|(?<!\w)\'/', ' ', text())
    #Removes all grammar except apostrophes
    letters_only_decontracted = decontracted(letters_only)
    #Expands out contracted words like can't to can not
    remove_apost = re.sub("[^a-zA-Z' ]+", ' ', letters_only_decontracted)
    #Removes apostrphes
    lower_case = remove_apost.lower()
    #Makes lower case
    words = lower_case.split()
    #Splits array into each word
    meaningfulWords = [w for w in words if not w in stopwords.words("english")]
    #Removes all stopwords from list of words leaving only meaningful ones (hopefully)
    return" ".join(meaningfulWords)


num_articles = train["text"].size
clean_train_articles = []

print("Cleaning and parsing articles...\n")
for i in range(0, num_articles):
    #if train["text"][i] != "":
        # Goes through each article and runs the function on them then stores to array
        print("Article %d of %d" % (i + 1, num_articles))
        clean_train_articles.append(article_cleanup(train["text"][i]))
        # print(article_cleanup(data["article-text"][i]))
        if train["label"][i] == 1:
            print("Fake article \n")
        else:
            print("Real article \n")
   # else:
    #    print("\nArticle %d of %d" % (i + 1, num_articles) + " invalid")

print("Creating the bag of words for training data...\n")
vectorizer = CountVectorizer(analyzer="word", tokenizer=None, preprocessor=None, stop_words=None, max_features=5000)
# This sets the parameters for the vectors
train_data_features = vectorizer.fit_transform(clean_train_articles)
# Turns clean articles into a document term matrix
train_data_features = train_data_features.toarray()
# Appends matrix to array
print("Articles, number of words =", train_data_features.shape)
vocab = vectorizer.get_feature_names()
dist = np.sum(train_data_features, axis=0)
for tag, count in zip(vocab, dist):
    print(count, tag)

forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit(train_data_features, train["label"])

num_articles = test["text"].size
print(test.shape)
clean_test_articles = []
print("Cleaning and parsing the test set article authenticity...\n")
for i in range(0, num_articles):
    print("Article %d of %d\n" % (i+1, num_articles))
    clean_review = article_cleanup(test["text"][i])
    clean_test_articles.append(clean_review)

test_data_features = vectorizer.transform(clean_test_articles)
test_data_features = test_data_features.toarray()

result = forest.predict(test_data_features)
output = pd.DataFrame(data={"id": test["id"], "label": result})
output.to_csv("outputs/UseCase4-1ForestOutput.csv", index=False, quoting=3)

estimator = forest.estimators_[10]

export_graphviz(estimator, out_file='UseCase4-1Tree.dot', feature_names = vectorizer.get_feature_names(),
                rounded = True, proportion = False, precision = 2, filled = True)

(graph,) = pydot.graph_from_dot_file('UseCase4-1Tree.dot')
graph.write_png('UseCase4-1Tree.png')