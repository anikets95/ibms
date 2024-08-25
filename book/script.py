import pickle
import pandas as pd
from sklearn.neighbors import NearestNeighbors


def model_fn(model_dir):
    with open(f'{model_dir}/knn_model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model


def predict_fn(input_data, model):
    return model.kneighbors(input_data, n_neighbors=5)[1]
