from sklearn.tree import DecisionTreeRegressor
import numpy as np

class UserSegmentor(DecisionTreeRegressor):
    def __init__(self, criterion='squared_error', splitter='best', max_depth=None, 
                 min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0,
                 max_features=None, random_state=None, max_leaf_nodes=None, 
                 min_impurity_decrease=0.0, ccp_alpha=0.0):
        super(UserSegmentor, self).__init__(
            criterion=criterion, splitter=splitter, max_depth=max_depth,
            min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf,
            min_weight_fraction_leaf=min_weight_fraction_leaf, max_features=max_features,
            random_state=random_state, max_leaf_nodes=max_leaf_nodes,
            min_impurity_decrease=min_impurity_decrease, ccp_alpha=ccp_alpha
        )

    def predict(self, X, return_rules=True):
        if self.tree_ is None:
            raise NotFittedError("This DecisionTreeRegressor instance is not fitted yet.")
        
        def recurse_find_path(node, conditions, sample):
            if self.tree_.feature[node] != -2:  # -2 means it's a leaf node
                feature_index = self.tree_.feature[node]
                name = self.feature_names_in_[feature_index]
                threshold = self.tree_.threshold[node]
                if sample[name] <= threshold:
                    conditions.append((name, "<=", threshold))
                    return recurse_find_path(self.tree_.children_left[node], conditions, sample)
                else:
                    conditions.append((name, ">", threshold))
                    return recurse_find_path(self.tree_.children_right[node], conditions, sample)
            else:
                return self.format_conditions(conditions)

        if return_rules:
            if not hasattr(self, 'feature_names_in_'):
                raise ValueError("Feature names are not available. Ensure the model was fitted with feature names.")
            rules = [recurse_find_path(0, [], row) for _, row in X.iterrows()]
            return np.array(rules)
        else:
            return super().predict(X)

    def format_conditions(self, conditions):
        if not conditions:
            return "No conditions available"
        return ' and '.join([f"{feat} {op} {th:.2f}" for feat, op, th in conditions])
