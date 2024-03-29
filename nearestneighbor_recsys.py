# -*- coding: utf-8 -*-
"""NearestNeighbor-RecSys

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UZcCK58o0lxBqKunzrjGoVqtte3uDZ61
"""

import pandas as pd
import numpy as np

df = pd.read_csv("SalesData1.csv",error_bad_lines=False)
df.head()

df_1 = pd.read_excel("RIDGE.xlsx")
df_1.head()

combine_movie_rating = df_1.dropna(axis = 0, subset = ['item_id'])

movie_ratingCount = (combine_movie_rating.
     groupby(by = ['item_id'])['product_type'].
     count().
     reset_index().
     rename(columns = {'product_type': 'TypeOfSku'})
     [['item_id', 'TypeOfSku']]
    )

movie_ratingCount.head()

rating_with_totalRatingCount = combine_movie_rating.merge(movie_ratingCount, left_on = 'item_id', right_on = 'item_id', how = 'left')
rating_with_totalRatingCount.head()

pd.set_option('display.float_format', lambda x: '%.3f' % x)
print(rating_with_totalRatingCount['price'].describe())

popularity_threshold = 50
rating_popular_movie= rating_with_totalRatingCount.query('price >= @popularity_threshold')
rating_popular_movie.head()

movie_features_df=rating_popular_movie.pivot_table(index='item_id',columns='qty_ordered',values='price').fillna(0)
movie_features_df.head()

from scipy.sparse import csr_matrix

movie_features_df_matrix = csr_matrix(movie_features_df.values)

from sklearn.neighbors import NearestNeighbors


model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(movie_features_df_matrix)

movie_features_df.shape

query_index = np.random.choice(movie_features_df.shape[0])
print(query_index)
distances, indices = model_knn.kneighbors(movie_features_df.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 6)

movie_features_df.head()

for i in range(0, len(distances.flatten())):
    if i == 0:
        print('Recommendations for {0}:\n'.format(movie_features_df.index[query_index]))
    else:
        print('{0}: {1}, with distance of {2}:'.format(i, movie_features_df.index[indices.flatten()[i]], distances.flatten()[i]))

