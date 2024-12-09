from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from collections import Counter
# Download stopwords if not already done
nltk.download('stopwords')
nltk.download('punkt')

custom_words_to_remove=["and","that"]
STOP_WORDS = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
def removeStopWords(text):
    #text=  "This is an example sentence, demonstrating stop word removal."
    words = word_tokenize(text)
    stop_words = set(STOP_WORDS)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    filtered_words = [word for word in filtered_words if word.isalnum()]
    return filtered_words
    

def countWordFrequency(content):
    count = Counter(content)
    return count
def removeCustomwords(words):
      words = set(words)
      filtered_words = [word for word in words if word not in custom_words_to_remove]
      return filtered_words



