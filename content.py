# %%
import pandas as pd
import requests
import json
import re
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval    
import scipy
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import requests
from PIL import Image
from io import BytesIO

# %%
df = pd.read_csv('C:/Users/ASUS/Desktop/Books/GoodReads_100k_books.csv')
df.head()

# %%
df.isnull().sum()

# %%
df.fillna(value="",inplace=True)

# %%
a=[]
def collect(str):
    a.append(str.split(','))
genre_data = df['genre'].apply(collect)
a

# %%
import itertools

b = list(itertools.chain.from_iterable(a))
b = [genre for genre in b if genre]# Removing empty strings



# %%

empty = set()  # Initialize an empty set

for item in b:  # Iterate over the elements, not indices
    empty.add(item)  # Add each genre to the set
new_list = list(empty)
print(len(new_list))


# %%

df['desc'] = df['desc'].fillna('')
def clean_text(text):
    text = str(text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip().lower()

df['desc'] = df['desc'].apply(clean_text)

# %%
df["genre"] = df["genre"].apply(lambda x: literal_eval(x) if isinstance(x, str) and x.startswith("[") else x.split(','))


# %%
def genre_to_string(genres):
    return " ".join(genres) if isinstance(genres, list) else genres

df["genre"] = df["genre"].apply(genre_to_string)

# %%
mlb=MultiLabelBinarizer()
genre_features=mlb.fit_transform(df['genre'])

# %%
tfidf = TfidfVectorizer(stop_words='english',max_features=5000)
desc_features=tfidf.fit_transform(df['desc'])

# %%
import scipy.sparse
combined_features=scipy.sparse.hstack([genre_features,desc_features]).tocsr()

# %%
knn = NearestNeighbors(metric='cosine',algorithm='brute')
knn.fit(combined_features)


# %%
def recommend_content_based(title, top_n=20):
    idx = df[df['title'] == title].index[0]
    query = combined_features[idx].reshape(1,-1)
    distances, indices = knn.kneighbors(query, n_neighbors=top_n+1)
    return df[['title', 'genre', 'desc', 'rating', 'totalratings','img','link','author']].iloc[indices[0][1:]]

print(recommend_content_based('Tyneham'))
