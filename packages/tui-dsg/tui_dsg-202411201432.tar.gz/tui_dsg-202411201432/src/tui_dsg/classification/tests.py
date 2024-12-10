import numpy as np
import pandas as pd
from checkmarkandcross import image
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


def aufgabe1(df: pd.DataFrame, df_train: pd.DataFrame, df_test: pd.DataFrame):
    return image(isinstance(df, pd.DataFrame)
                 and isinstance(df_train, pd.DataFrame)
                 and isinstance(df_test, pd.DataFrame)
                 and len(df) == 1009
                 and 2.9 < len(df_train) / len(df_test) < 3.1)


def aufgabe2(nn: KNeighborsClassifier, nn_accuracy: float):
    return image(isinstance(nn, KNeighborsClassifier)
                 and isinstance(nn_accuracy, float) and 0.67 < nn_accuracy < 1)


def aufgabe3(tree: DecisionTreeClassifier, tree_accuracy: float):
    return image(isinstance(tree, DecisionTreeClassifier)
                 and isinstance(tree_accuracy, float) and 0.5 < tree_accuracy < 1)


def aufgabe4(nn_prediction: np.ndarray, tree_prediction: np.ndarray):
    return image(isinstance(nn_prediction, np.ndarray)
                 and not nn_prediction.any()
                 and isinstance(tree_prediction, np.ndarray)
                 and tree_prediction.all())


def aufgabe5(nn_precision: float, nn_recall: float, tree_precision: float, tree_recall: float):
    return image(isinstance(nn_precision, float)
                 and 0.57 < nn_precision < 0.62
                 and isinstance(nn_recall, float)
                 and 0.30 < nn_recall < 0.35
                 and isinstance(tree_precision, float)
                 and 0.36 < tree_precision < 0.41
                 and isinstance(tree_recall, float)
                 and 0.38 < tree_recall < 0.43)
