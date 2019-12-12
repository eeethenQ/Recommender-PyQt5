# -*- coding: utf-8 -*-
import sys, os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from MainWindows import Ui_Dialog

# data science imports
import math
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD

# utils import
from fuzzywuzzy import fuzz

# Image Grid
from image import save_img



class MainWindow(QMainWindow, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Button
        self.Exit.clicked.connect(QApplication.instance().quit)
        self.rec_knn.clicked.connect(self.recommend_knn)
        self.rec_svd.clicked.connect(self.recommend_svd)

        self.show()

    def recommend_svd(self):
        movie_name = self.lineEdit.text()
        print(movie_name)

        #Make Recommendation
        movie_to_idx, movie_user_mat_sparse, id_to_imdbid = load_data()
        model_svd = TruncatedSVD(n_components=12, random_state=17)
        recom_movie_name = make_recommendation_svd(
            model = model_svd,
            data = movie_user_mat_sparse,
            fav_movie = movie_name,
            mapper = movie_to_idx,
            n_recommendations = 10
        )

        # Generate Text output 
        idx_to_movie = {v: k for k, v in movie_to_idx.items()}
        # output_text = "Recommend begin!\n -------------------\n"
        output_text = ""
        id = []
        for i, name in enumerate(recom_movie_name):
            id.append(movie_to_idx[name])
            output_text += "{} : {}\n".format(i+1, name)
        
        # write to textedit
        self.textEdit.clear()
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.insertText(output_text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

        # make image grid
        self.img.clear()
        imdbid = [id_to_imdbid[i][0] for i in id]
        save_img("./tmp.jpg", imdbid)
        self.show_img("./tmp.jpg")

    def recommend_knn(self):
        movie_name = self.lineEdit.text()
        print(movie_name)

        #Make Recommendation
        movie_to_idx, movie_user_mat_sparse, id_to_imdbid = load_data()
        model_knn = NearestNeighbors(metric = "cosine", algorithm = "brute", n_neighbors = 5, n_jobs = -1)
        raw_recommends = make_recommendation_knn(
            model = model_knn,
            data = movie_user_mat_sparse,
            fav_movie = movie_name,
            mapper = movie_to_idx,
            n_recommendations = 10
        )

        # Generate Text output 
        idx_to_movie = {v: k for k, v in movie_to_idx.items()}
        # output_text = "Recommend begin!\n -------------------\n"
        output_text = ""
        id = []
        for i, (idx, dist) in enumerate(raw_recommends):
            id.append(idx)
            output_text += "{} : {}\n".format(i+1, idx_to_movie[idx])
        
        # write to textedit
        self.textEdit.clear()
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(output_text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

        # make Image grid
        self.img.clear()
        imdbid = [id_to_imdbid[i][0] for i in id]
        save_img("./tmp.jpg", imdbid)
        self.show_img("./tmp.jpg")

    def show_img(self, path):
        pixmap = QPixmap(path)
        lbl = self.img
        lbl.setPixmap(pixmap)

def load_data():

    data_path = "./ml-latest-small"
    movies_filename = 'movies.csv'
    ratings_filename = 'ratings.csv'
    imdb_filename = 'links.csv'
    df_movies = pd.read_csv(
        os.path.join(data_path, movies_filename),
        usecols=['movieId', 'title'],
        dtype={'movieId': 'int32', 'title': 'str'})

    df_ratings = pd.read_csv(
        os.path.join(data_path, ratings_filename),
        usecols=['userId', 'movieId', 'rating'],
        dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})
    
    df_imdb = pd.read_csv(
        os.path.join(data_path, imdb_filename),
        usecols = ['movieId', 'imdbId'],
        dtype = {'movieId': 'int32', 'imdbId': 'int32'})

    # pivot and create movie-user matrix
    movie_user_mat = df_ratings.pivot(index='movieId', columns='userId', values='rating').fillna(0)
    # create mapper from movie title to index
    movie_to_idx = {
        movie: i for i, movie in 
        enumerate(list(df_movies.set_index('movieId').loc[movie_user_mat.index].title))
    }

    # movie Id to IMDB ID in order to retrieve the image of poster
    id_to_imdbid = df_imdb.set_index('movieId').T.to_dict('list')

    # transform matrix to scipy sparse matrix
    movie_user_mat_sparse = csr_matrix(movie_user_mat.values)

    return movie_to_idx, movie_user_mat_sparse, id_to_imdbid

def fuzzy_matching(mapper, fav_movie, verbose=True):

    match_tuple = []
    # get match
    for title, idx in mapper.items():
        ratio = fuzz.ratio(title.lower(), fav_movie.lower())
        if ratio >= 60:
            match_tuple.append((title, idx, ratio))
    # sort
    match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
    if not match_tuple:
        print('Oops! No match is found')
        return
    if verbose:
        print('Found possible matches in our database: {0}\n'.format([x[0] for x in match_tuple]))
    
    return match_tuple[0][1]


def make_recommendation_svd(model, data, mapper, fav_movie, n_recommendations):
    # fit
    matrix = model.fit_transform(data)
    # get input movie index
    print('You have input movie:', fav_movie)
    idx = fuzzy_matching(mapper, fav_movie, verbose=True)
    # inference
    print('Recommendation system start to make inference')
    print('......\n')
    corr = np.corrcoef(matrix)
    recom_movie_idx = np.argsort(corr[idx])[-n_recommendations-1: -1]
    # get reverse mapper
    reverse_mapper = {v: k for k, v in mapper.items()}
    # print recommendations
    recom_movie_name = [reverse_mapper[i] for i in np.flip(recom_movie_idx)]
    print('Recommendations for {}:'.format(fav_movie))
    for i, name in enumerate(recom_movie_name):
        print('{0}: {1}, with closeness of {2}'.format(i+1, name, corr[idx][recom_movie_idx[-1-i]]))
    return recom_movie_name

def make_recommendation_knn(model, data, mapper, fav_movie, n_recommendations):

    # fit
    model.fit(data)
    # get input movie index
    print('You have input movie:', fav_movie)
    idx = fuzzy_matching(mapper, fav_movie, verbose=True)
    # inference
    print('Recommendation system start to make inference')
    print('......\n')
    distances, indices = model.kneighbors(data[idx], n_neighbors=n_recommendations+1)
    # get list of raw idx of recommendations
    raw_recommends = \
        sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[1::1]
    
    # get reverse mapper
    reverse_mapper = {v: k for k, v in mapper.items()}
    # print recommendations
    print('Recommendations for {}:'.format(fav_movie))
    for i, (idx, dist) in enumerate(raw_recommends):
        print('{0}: {1}, with distance of {2}'.format(i+1, reverse_mapper[idx], dist))
    
    return raw_recommends


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Recommander")

    windows = MainWindow()
    sys.exit(app.exec_())
