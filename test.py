import flask, pandas, sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

docs = ["black casio calculator lab 2", "black scientific calculator lab 2", "blue water bottle"]
tfidf = TfidfVectorizer().fit_transform(docs)
print(cosine_similarity(tfidf[0], tfidf))
print("Flask", flask.__version__, "| pandas", pandas.__version__, "| scikit-learn", sklearn.__version__)
