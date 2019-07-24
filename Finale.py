import pandas as pd
from newspaper import Article
import re

# Reading the article using the URL....
url = input("Enter URL:")  # Prompts Enter URL: on the screen
article = Article(url)  # save article on url in variable 'article'
article.download()  # Downloads article
article.parse()  # Reads the article

Text = article.text.lower()  # Converting text of the article to lower case

print("\n----------------------------------------------------------------------------\n")
print("\nArticle's Title:\n" + article.title)
print("\nArticle's Text:\n" + Text)
print("\n----------------------------------------------------------------------------\n")

#Syntactic Negations
Syntactic = pd.Series(
    ["needs a", "needs to", "could have", "could've", "should have", "should've", "would have", "would've", '-less ',
     'no ', 'not ', 'rather ', "couldn’t ", "wasn’t ", "didn’t ", "wouldn’t ", "shouldn’t ", "weren’t ", "don’t ",
     "doesn’t ", "haven’t ", "hasn’t ", "won’t ", 'wont ', "hadn’t ", 'never ', 'none ', 'nobody ', 'nothing ',
     'neither ', 'nor ', 'nowhere ', "isn’t ", "can’t ", 'cannot ', "mustn’t ", "mightn’t ", "shan’t ", 'without ',
     "needn’t ", 'de-', 'dis-', 'il-', 'im-', 'in-', 'ir-', 'mis-', 'non-', 'un-'])               

#Exceptions to Negation
Negation_Exceptions = pd.Series(["not just", "not only", "no wonder", "not to mention"])

#Diminishers
Diminishers = pd.Series(['hardly', 'less', 'little', 'rarely', 'scarcely', 'seldom'])

#Contrating Conjunctions
Contrasting_conj = pd.Series(
    ['but', 'however', 'in contrast', 'instead', 'on the other hand', 'whereas', 'except that', 'on the contrary',
     'conversely', 'nevertheless', 'although', 'alternatively'])

#Punctuations
Punctuations = pd.Series([';', ':', '!', '?', ','])

#Stop Words
stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at",
              "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do",
              "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have",
              "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself",
              "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its",
              "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other",
              "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's",
              "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
              "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those",
              "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've",
              "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom",
              "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
              "yourself", "yourselves"]

# Detecting conjunctions and punctuations in main text of the Article
for w in Contrasting_conj:
    if w in Text:
        Text = Text.replace(w, ' *.* ')

for w in Punctuations:
    if w in Text:
        Text = Text.replace(w, '.')

# Splitting the main text of article into sentences
Sentences = Text.split('.')

# Reading positive and negative Lexicon Dictionaries from a location on pc (download the files and paste the location of the files)
positive_words = open('/home/highness/Desktop/positive-words.txt', 'r').read().split()
negative_words = open('/home/highness/Desktop/negative-words.txt', 'r').read().split()

# Declaring positive and negative sentiment score variables
pos = 0
neg = 0

# Dictionary with Sentences and their Negation score(-1 if negation is there and 1 if negation is not there)
Sentences1 = {"Sentence": "Negation Score"}

# List of Positive and Negative words found
positive_words_found = []
negative_words_found = []

# Updating Dictionay "Sentences1" with respective sentences negation score
for s in Sentences:
    Sentences1.update({s: 1})
    for w in Syntactic:
        if w in s:  # If syntactic negation is present
            if Sentences1[s] == -1:  # If sentence has -1 negation score already, i.e. odd number of negation words has occured
                Sentences1[s] = 1
            else:
                Sentences1[s] = -1
    for x in Negation_Exceptions:  # Taking care of negation exceptions
        if x in s:
            if Sentences1[s] == 1:
                Sentences1[s] = -1
            else:
                Sentences1[s] = 1
    for w in Diminishers:  # Taking care of Diminishers
        if w in s:
            Sentences1[s] *= 0.5
    if s[0:2] == '* ':  # Taking care of Conjunctions in Sentences
        Sentences1[s] *= 1.5
    if s[-2:] == ' *':
        Sentences1[s] *= 0.5

# Getiing Sentiment score using Bag_of_words Technique

for s in Sentences1:
    Bag_of_words = {"Word": "Frequency"}
    clean_Bag_of_Words = {"Word": "Frequency"}
    Words_in_Text = re.findall(r'\w+', s)
    for w in Words_in_Text:
        if w in Bag_of_words:
            Bag_of_words[w] += 1
        else:
            Bag_of_words[w] = 1
    for w in Bag_of_words:
        if w not in stop_words:
            clean_Bag_of_Words.update({w: Bag_of_words[w]})
    for w in clean_Bag_of_Words:
        if w in positive_words:
            if Sentences1[s] >= 0:
                pos += Sentences1[s] * clean_Bag_of_Words[w]
                positive_words_found.append(w)
            else:
                neg += -Sentences1[s] * clean_Bag_of_Words[w]
                negative_words_found.append("negation of " + w)
        elif w in negative_words:
            if Sentences1[s] >= 0:
                neg += Sentences1[s] * clean_Bag_of_Words[w]
                negative_words_found.append(w)
            else:
                pos += -Sentences1[s] * clean_Bag_of_Words[w]
                positive_words_found.append("negation of " + w)

if pos != 0 or neg != 0:
    Sentiment_Score = (pos - neg) / (pos + neg)
else:
    Sentiment_Score = 0

positive_words_found = pd.DataFrame(positive_words_found, columns=["Words"])
negative_words_found = pd.DataFrame(negative_words_found, columns=['Words'])

print("\nPositive Sentiments/Words found:\n")
print(positive_words_found)
print("\n----------------------------------------------------------------------------\n")
print("\nNegative Sentiments/Words found:\n")
print(negative_words_found)
print("\n----------------------------------------------------------------------------\n")
print("Positive sentiment score: ")
print(pos)
print("Negative sentiment score: ")
print(neg)
print("\n----------------------------------------------------------------------------\n")
print("Overall Sentiment Score: ")
print(Sentiment_Score)
print("\n----------------------------------------------------------------------------\n")
