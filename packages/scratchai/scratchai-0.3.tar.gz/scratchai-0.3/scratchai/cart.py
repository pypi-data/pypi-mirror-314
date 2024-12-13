import numpy as np
from collections import Counter

# static helpers functions
def _to_numeric(array):
    try:
        return array.astype('float')
    except:
        return array
    
def _most_common(array):
    count = Counter(array)
    return count.most_common(1)[0][0]

# Tree metrics functions
def entropy(y):
    uniques, counts = np.unique(y, return_counts = True)
    p = counts / len(y)
    return abs(-np.sum(p * np.log2(p)))

def infromation_gain(y, y_left, y_right):
    w = len(y_left) / len(y)
    return entropy(y) - (w * entropy(y_left) + (1 - w) * entropy(y_right))

def _mean_squared_error(y_true, y_pred):
    return np.sum((y_pred - y_true) ** 2) / len(y_true)

# Tree nodes
class _DecisionNode:
    def __init__(self, feature = None, value = None, left = None, right = None):
        self.feature = feature
        self.value = value
        self.left = left
        self.right = right
        
class _LeafNode:
    def __init__(self, value = None):
        self.value = value

# Incomplete - Todo: provide doc strings for both tree classes methods.
class DecisionTreeClassifier:
    def __init__(self, max_depth = 50, min_samples_split = 5):
        # thr root node of th three
        self.root = None
        
        # the tree parameters
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        
        # features data types
        self.dtypes = []
        
    def _init_dtypes(self, X):
        for i in range(X.shape[1]):
            cur_column = _to_numeric(X[:, i])
            if (isinstance(cur_column.dtype, np.dtypes.Int64DType) or 
                isinstance(cur_column.dtype, np.dtypes.Float64DType)):
                self.dtypes.append('numeric')
            else:
                self.dtypes.append('categorical')
                
    def fit(self, X, y):
        # initialize the features data types and grow the three
        self._init_dtypes(X)
        self.root = self._grow_tree(X, y)
        
    def _grow_tree(self, X, y, depth = 0):
        n_samples, n_labels = X.shape[0], len(np.unique(y))
        
        # Checks Three criteria :
        # 1 - if the maximum depth exceeded
        # 2 - if the number of samples is insuffisant for split
        # 3 - if there no further slit needed
        # and returns a leaf node if one of them is True.
        if depth >= self.max_depth or n_samples <= self.min_samples_split or n_labels == 1:
            leaf_val = _most_common(y)
            return _LeafNode(value = leaf_val)
        
        # finds the best split
        split_feature, split_val = self._best_split(X, y)
        
        left_indices, right_indices = self._split(split_feature, split_val, _to_numeric(X[:, split_feature]))
        X_left, X_right = X[left_indices], X[right_indices]
        y_left, y_right = y[left_indices], y[right_indices]
        
        parent_node = _DecisionNode(split_feature, split_val)
        parent_node.left = self._grow_tree(X_left, y_left)
        parent_node.right = self._grow_tree(X_right, y_right)
        
        return parent_node
        
    def _best_split(self, X, y):
        n_features = X.shape[1]
        split_gain = 0
        split_feature, split_val = None, None
        
        for feature in range(n_features):
            cur_column = _to_numeric(X[:, feature])
            
            if self.dtypes[feature] == 'numeric':
                # get all the possible thresholds for feature
                cur_column.sort()                
                uniques = np.unique(cur_column)
                thresholds = (uniques[:-1] + uniques[1:]) / 2
                
                for threshold in thresholds:
                    # split the data using the current threshold
                    left_indices, right_indices = self._split(feature, threshold, cur_column)
                    y_left, y_right = y[left_indices], y[right_indices]
                    
                    # calcualate the information gain of splitting y into y_left and y_right
                    gain = infromation_gain(y, y_left, y_right)
                    
                    if gain > split_gain:
                        split_gain = gain
                        split_feature, split_val = feature, threshold
                        
            else:
                # get all the unique values of the current feature
                uniques = np.unique(cur_column)
                
                for val in uniques:
                    # split the data using the current val
                    left_indices, right_indices = self._split(feature, val, cur_column)
                    y_left, y_right = y[left_indices], y[right_indices]
                    
                    # calcualate the information gain of splitting y into y_left and y_right
                    gain = infromation_gain(y, y_left, y_right)
                    
                    if gain > split_gain:
                        split_gain = gain
                        split_feature, split_val = feature, val
        
        return split_feature, split_val                    
                
    def _split(self, feature, value, column):
        left_indices = column >= value if self.dtypes[feature] == 'numeric' else column == value
        right_indices = column < value if self.dtypes[feature] == 'numeric' else column != value
        return left_indices, right_indices
    
    def predict(self, X):
        return np.array([self._traverse_tree(row, self.root) for row in X])
    
    def _traverse_tree(self, X, node):
        if isinstance(node, _LeafNode):
            return node.value
        
        if self.dtypes[node.feature] == 'numeric':
            if float(X[node.feature]) >= node.value:
                return self._traverse_tree(X, node.left)
            return self._traverse_tree(X, node.right)
        else:
            if X[node.feature] == node.value:
                return self._traverse_tree(X, node.left)
            return self._traverse_tree(X, node.right)
        
class DecisionTreeRegressor:
    def __init__(self, min_samples_split = 20, max_depth = 50):
        # Tree root
        self.root = None
        
        # Tree parameters
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        
        # features data types
        self.dtypes = []
        
    def _init_dtypes(self, X):
        for i in range(X.shape[1]):
            cur_column = _to_numeric(X[:, i])
            if (isinstance(cur_column.dtype, np.dtypes.Int64DType) or 
                isinstance(cur_column.dtype, np.dtypes.Float64DType)):
                self.dtypes.append('numeric')
            else:
                self.dtypes.append('categorical')
                
    def fit(self, X, y):
        # initialize the features data types and grow the three
        self._init_dtypes(X)
        self.root = self._grow_tree(X, y)
        
    def _grow_tree(self, X, y, depth = 0):
        n_samples, uniques = X.shape[0], len(np.unique(y))
        
        # Checks Three criteria :
        # 1 - if the maximum depth exceeded
        # 2 - if the number of samples is insuffisant for split
        # 3 - if there no further slit needed
        # and returns a leaf node if one of them is True.
        if depth >= self.max_depth or n_samples <= self.min_samples_split or uniques == 1:
            leaf_val = np.mean(y)
            return _LeafNode(value = leaf_val)
        
        split_feature, split_val = self._best_split(X, y)
        left_indices, right_indices = self._split(split_feature, split_val, _to_numeric(X[:, split_feature]))
        
        X_left, X_right = X[left_indices], X[right_indices]
        y_left, y_right = y[left_indices], y[right_indices]
        
        left_node, right_node = self._grow_tree(X_left, y_left, depth + 1), self._grow_tree(X_right, y_right, depth + 1)
        return _DecisionNode(split_feature, split_val, left_node, right_node)
    
    def _split(self, feature, value, column):
        left_indices = column >= value if self.dtypes[feature] == 'numeric' else column == value
        right_indices = column < value if self.dtypes[feature] == 'numeric' else column != value
        return left_indices, right_indices
    
    def _best_split(self, X, y):
        n_features = X.shape[1]
        split_feature, split_val = None, None
        split_error = float('-inf')
        
        for feature in range(n_features):
            cur_column = _to_numeric(X[:, feature])
            
            if self.dtypes[feature] == 'numeric':
                cur_column.sort()
                uniques = np.unique(cur_column)
                thresholds = (uniques[1:] + uniques[:-1]) / 2
                
                for threshold in thresholds:
                    left_mean, right_mean = np.mean(y[cur_column >= threshold]), np.mean(y[cur_column < threshold])
                    y_pred = np.array([left_mean if val >= threshold else right_mean for val in cur_column])
                    error = _mean_squared_error(y, y_pred)
                    
                    if error < split_error:
                        split_error = error
                        split_feature, split_val = feature, threshold
                        
            else:
                uniques = np.unique(cur_column)
                
                for value in uniques:
                    left_mean, right_mean = np.mean(y[cur_column == value]), np.mean(y[cur_column != value])
                    y_pred = np.array([left_mean if value == val else right_mean for val in cur_column])
                    error = _mean_squared_error(y, y_pred)
                    
                    if error > split_error:
                        split_error = error
                        split_feature, split_val = feature, value
                        
        return split_feature, split_val
    
    def predict(self, X):
        return np.array([self._traverse_tree(row, self.root) for row in X])
    
    def _traverse_tree(self, X, node):
        if isinstance(node, _LeafNode):
            return node.value
        
        if self.dtypes[node.feature] == 'numeric':
            if float(X[node.feature]) >= node.value:
                return self._traverse_tree(X, node.left)
            return self._traverse_tree(X, node.right)
        else:
            if X[node.feature] == node.value:
                return self._traverse_tree(X, node.left)
            return self._traverse_tree(X, node.right)
        