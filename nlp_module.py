import re
import nltk
from joblib import load
nltk.download('stopwords')
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize.toktok import ToktokTokenizer

tfidf_vect = load('tfidf-word.joblib')
svmword = load('svm-analyzer.joblib')

english_stopwords = set(nltk.corpus.stopwords.words('english'))
tokenizer = ToktokTokenizer()
porterStemmer = nltk.porter.PorterStemmer()

def remove_stopwords(text, is_lower = False):
  tokens = tokenizer.tokenize(text)
  tokens = [token.strip() for token in tokens]
  if is_lower:
    filtered_tokens = [token for token in tokens if token not in english_stopwords]
  else:
    filtered_tokens = [token for token in tokens if token.lower() not in english_stopwords]

  # stitch back the text
  filtered_tokens = ' '.join(filtered_tokens)
  return filtered_tokens

def preprocess(text):
  soup = BeautifulSoup(text, 'html.parser')
  no_symbols = re.sub('[^0-9a-zA-Z:\s]', '', soup.get_text()).strip()
  stemed_text = ' '.join([porterStemmer.stem(word) for word in no_symbols.split()])
  return remove_stopwords(stemed_text)

def guess_sentiment(review):
  result = svmword.predict(tfidf_vect.transform([preprocess(review)]))[0]
  target_name = ['Positive', 'Negative']
  return target_name[result]
