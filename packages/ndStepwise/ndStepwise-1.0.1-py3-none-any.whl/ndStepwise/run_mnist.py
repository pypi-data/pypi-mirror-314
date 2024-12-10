import pandas as pd
import concurrent.futures
import numpy as np
import math
from sklearn.model_selection import train_test_split, cross_val_predict, cross_val_score, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_curve, ConfusionMatrixDisplay, auc, roc_auc_score, f1_score
from sklearn import datasets
from statistics import mean
from ndStepwise.includes import model as mod
import pandas as pd
from joblib import dump, load
from ndStepwise.includes.config import Config
from ndStepwise.includes import model_functions as mf
import time
from itertools import combinations
import random
from graphviz import Digraph
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
from datetime import datetime 
import os
import argparse
from tensorflow.keras.datasets import mnist

def main(model_types):
    # config.log.info('Max Rocks')
    # config.log.error('This is an extra long message about how there was an error because Max wants to see if there is a weird format when messages get extra long.')
    # config.log.debug('THIS SHOULDNT LOG')
    # return
    filename = 'MNIST'
    print(filename)
    if len(filename) <= 1:
        raise Exception(f"Improper filename of: {filename}")
    start = time.perf_counter()
   
    dataset = filename
    config = Config(dataset)
    config.log.info(f'Beginning of {dataset}.')

    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    # Flatten the 28x28 images into a single 784-length vector per image
    X_train_flattened = X_train.reshape(X_train.shape[0], -1)
    X_test_flattened = X_test.reshape(X_test.shape[0], -1)

    # Convert to a Pandas DataFrame
    X_train_df = pd.DataFrame(X_train_flattened)
    X_test_df = pd.DataFrame(X_test_flattened)

    # Optionally, add column names (e.g., "pixel_0", "pixel_1", ..., "pixel_783")
    X_train_df.columns = [f"pixel_{i}" for i in range(X_train_flattened.shape[1])]
    X_test_df.columns = [f"pixel_{i}" for i in range(X_test_flattened.shape[1])]

    # Add the labels as a separate column if desired
    X_train_df['Y'] = y_train
    X_test_df['Y'] = y_test
    X_train = X_train_df
    X_test = X_test_df
    y_test = y_test

    categories = tuple(X_train['Y'].unique())
    score_type = 'accuracy'
    transform_label = None
    
    config.log.info('Beginning of stepwise tree finder.')
    best_tree = mf.stepwise_tree_finder(config, categories, X_train, [], {}, model_types=model_types, score_type=score_type)
    config.log.info('Finished stepwise tree finder.')
    config.log.info(f"Took: {round(time.perf_counter()-start,3)} to do find best tree.")
    model_strucs = list(best_tree.keys())
    tree_types = list(best_tree.values())
    config.log.info(model_strucs)
    config.log.info(tree_types)
    best_trained_model = mf.build_best_tree(config, X_test, X_train, y_test, score_type, tree_types, model_strucs, categories, transform_label=transform_label)[0]
    mf.graph_model(config, best_trained_model, filename, transform_label=transform_label, model_types=model_types)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-m', '--model_types', type=str, nargs='*', default=['randomForest', 'LogisticRegression', 'xgboost'],
                         help='An optional list models to be tested out of randomForest, LogisticRegression, xgboost, svm.')
    args = parser.parse_args()
    main(args.model_types)