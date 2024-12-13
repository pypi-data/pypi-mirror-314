import numpy as np
import pandas as pd
import warnings

# Incomplete - Todod : provide a doc strings for transfoms and invert-transforms methods.
class StandardScaler:
    def __init__(self):
        self.std = dict()
        self.mean = dict()
        
    def transform(self, X, columns):
        for column in columns:
            # store the feature standard and the mean for inverse sacling
            self.std[column] = X[column].std()
            self.mean[column] = X[column].mean()
            
            # scale the feature using the stored standard and mean
            X.loc[:, column] = (X[column] - self.mean[column]) / self.std[column]
            
        return X
    
    def inverse_transform(self, X, columns):
        for column in columns:
            X[column] = (X[column] + self.mean[column] * self.std[column])
            
        return X
    
def polynomial_features(X, degree = 1, inetraction_term = False):
    poly_features = []
    
    for row in X:
        inter_term = 1
        poly_row = []
        for v in row:
            inter_term *= v
            poly_row += [v ** d for d in range(1, degree + 1)]
        if inetraction_term:
            poly_row.append(inter_term)
        poly_features.append(poly_row)
        
    return np.array(poly_features)

#  Incomplete - Todo : update the split data function to handle both pandas Dataframes and numpy arrays.
def split_data(X, split_size = 0.8):
    first_set = X.sample(frac = split_size)
    second_set = X.drop(first_set.index)
    return first_set.reset_index(drop = True), second_set.reset_index(drop = True)

def one_hot(data: pd.DataFrame, columns = []):
    """onehot encode columns in data and convert the resulted columns dtypes into int.

    Args:
        data (pd.DataFrame): the data to encode
        columns (list, optional): the specific columns in data to encode. Defaults to [].

    Returns:
        _type_: Dataframe with the encoded columns in the data
    """
    encoded_data = None
    if columns:
        encoded_data = pd.get_dummies(data, columns = columns)
        for col in columns:
            for val in data[col].unique():
                with warnings.catch_warnings():
                    warnings.filterwarnings(action = 'ignore', category = FutureWarning)
                    encoded_data.loc[:, f"{col}_{val}"] = encoded_data[f"{col}_{val}"].astype('int')
    else:
        encoded_data = pd.get_dummies(data).astype('int')
    
    return encoded_data