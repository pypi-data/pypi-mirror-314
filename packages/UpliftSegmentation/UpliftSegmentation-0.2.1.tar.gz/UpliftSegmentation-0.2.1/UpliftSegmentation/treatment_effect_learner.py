# treatment_effect_learner.py

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import Lasso
import statsmodels.api as sm
from UpliftSegmentation.user_segmentor import UserSegmentor
import matplotlib.pyplot as plt



class TreatmentEffectLearner:
    def __init__(self,df, outcome,  controls, heterogeneity_dims, treatment = None, incentive_var = None,  n_clusters = 5, n_dims = 2, base_model_type = 'xgboost',  min_cluster_share = None, n_key_features_y = 35):
        """
        Initializes the TreatmentEffectLearner with specified parameters.

        Parameters:
        - df: DataFrame containing the data.
        - outcome: The name of the outcome variable.
        - controls: List of names of control variables.
        - heterogeneity_dims: Dimensions to assess heterogeneity of treatment effects.
        - incentive_var: Optional; variable representing the amount spent on incentives (e.g., coupons). 
          If set, the model segments users by ROI, calculated as the incremental impact on the outcome variable 
          per incremental impact on the incentive_var.
        - n_clusters: Maximum number of clusters to form in segmentation.
        - base_model_type: Type of the model to fit, 'xgboost' or 'random_forest'.
        - final_model: The final model to be used after base models.
        - n_key_features_y: Number of key features to consider from Y.
        """
        self.df = df
        N= df.shape[0]
        if treatment is not None:
            self.df['variant'] = self.df[treatment]
        if N<100000:
            print(f'Warning: sample might be too small: N = {N}')
            
        df_train, df_temp = train_test_split(self.df, test_size=0.9, random_state=0)

# Step 2: Split the temporary set into test and estimation datasets
        df_test, df_estimation = train_test_split(df_temp, test_size=0.9, random_state=0)


        self.df_train = df_train
        self.df_test = df_test
        self.df_estimation = df_estimation

        #self.model = clone(model)
        self.outcome = outcome
        
        self.controls = controls
        self.incentive_var = incentive_var
        self.hat_models = {}
        self.n_clusters = n_clusters
        self.n_dims = n_dims
        self.potential_outcome = {}  # Dictionary that will collect all possible scenarios and average potential outcomes for each of them.
       
        self.base_model_type = base_model_type
     
        
        self.strongest_signals = {}
        self.all_clusters = {}
        if min_cluster_share is None:
            self.min_cluster_share = 1/n_clusters
        else:
            self.min_cluster_share = min_cluster_share
        self.short_controls = None
        self.n_key_features_y = n_key_features_y
        self.key_features_y = None
        self.clusters_effect = {}
        self.heterogeneity_dims = heterogeneity_dims 
        #create mapping from initital treatment variables to new ones
        self._treat_vars()
        #

    def  _treat_vars(self):
        variant_values = list(self.df['variant'].unique())
        treat_only = [item for item in variant_values if item != 0 and item != 'control']
        treat_names = []
        for i in range(len(treat_only)):
            treat = treat_only[i]
    
            self.df['variant_'+str(i)] = np.where(self.df['variant'] == treat, 1, 0)
            treat_names.append('variant_'+str(i))
        mapping_df = pd.DataFrame({
            'Initial treatment values': treat_only,
            'New treatment variables': treat_names
            })
        self.treat_mapping = mapping_df
    def _get_top_n_features(self, X, y, n=10):
    
        
    
    # Initialize and fit the RandomForestRegressor
        model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs = -1)
        model.fit(X, y)

    # Get feature importances from the model
        importances = model.feature_importances_

    # Create a list of feature names sorted by their importance scores
        feature_importances = sorted(zip(X.columns, importances), key=lambda x: x[1], reverse=True)

    # Extract only the top n feature names
        top_n_features = [feature[0] for feature in feature_importances[:n]]
    # Return the top n features
        return top_n_features
    def _get_top_n_features_lasso(self, X, y, n=40, alpha=0.1):
        """
        Identify and return the top n most important features using Lasso regression.
    
        Parameters:
        - X: pandas DataFrame or numpy array of predictor variables.
        - y: List, pandas Series, or numpy array of target variable.
        - n: Number of top features to return.
        - alpha: Regularization strength; must be a positive float. Regularization improves the conditioning
                of the problem and reduces the variance of the estimates. Larger values specify stronger
                regularization.
             
        Returns:
        - List of the names of the top n most important features based on the Lasso model.
        """
        # Initialize Lasso regressor with the given alpha value
        lasso = Lasso(alpha=alpha, random_state=42)

        # Fit Lasso model
        lasso.fit(X, y)

        # Get the magnitude of the coefficients
        feature_importance = np.abs(lasso.coef_)

        # Create a list of feature names and their importance scores
        features_importances = sorted(zip(X.columns, feature_importance), key=lambda x: x[1], reverse=True)

        # Extract only the top n feature names where the coefficient is not zero
        top_n_features = [feature for feature, importance in features_importances if importance != 0][:n]

        # Return the list of top n feature names
        return top_n_features

    def get_signals(self):
        """
        Fit the T-Learner models.

        Parameters:
        - X: Features (independent variables).
        - y: Outcome variable (dependent variable).
        - treatment: Treatment indicator (1 if treated, 0 if control).
        """
        # Separate the treated and control groups
        X = self.df_train[(self.df_train['variant'] == 'control') | (self.df_train['variant'] == 0)][self.controls]
        y = self.df_train[(self.df_train['variant'] == 'control') | (self.df_train['variant'] == 0)][self.outcome]

        self.short_controls = self._get_top_n_features_lasso(X, y)
        self.key_features_y = self._get_top_n_features( X, y, n = self.n_key_features_y)
        #self.key_features_y = self.controls
        X = self.df_train[(self.df_train['variant'] == 'control') | (self.df_train['variant'] == 0)][self.key_features_y]
        
            
        if self.base_model_type == 'xgboost':
            param_grid = {
                'n_estimators': [100,300, 500, 700],
                'max_depth': [3,  7, 9, 11, 15, 20],
                'learning_rate': [ 0.0001, 0.001, 0.01, 0.1],
                'subsample': [0.5, 0.7, 1.0],
                'n_jobs': [-1]
                            }

            model = XGBRegressor()
# Set up RandomizedSearchCV
            random_search = RandomizedSearchCV(estimator=model, param_distributions=param_grid,
                                   n_iter=20, cv=5, scoring='neg_mean_squared_error',
                                   n_jobs=-1, random_state=42)
            random_search.fit(X, y)
            #best_random = random_search.best_estimator_
            
            best_params = random_search.best_params_
            self.hat_models['control'] = XGBRegressor(**best_params)
            self.hat_models['control'].fit(X, y)

        elif self.base_model_type == 'random_forest':
            param_grid = {
                'n_estimators': [100,300],
                'max_depth': [3,  7, 9, 11,15],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
                'n_jobs': [-1]
                            }

            model = RandomForestRegressor(n_jobs = -1)
# Set up RandomizedSearchCV
            random_search = RandomizedSearchCV(estimator=model, param_distributions=param_grid,
                                      n_iter=20, cv=5, scoring='neg_mean_squared_error',
                                      n_jobs=-1, random_state=42)
            random_search.fit(X, y)
            best_random = random_search.best_estimator_
            best_params = random_search.best_params_
            
            self.hat_models['control'] = RandomForestRegressor(**best_params)
            self.hat_models['control'].fit(X, y)

        
        #self.hat_models['control'] = clone(model)
        
        for variant in self.treat_mapping['Initial treatment values']:
            #X = self.df_train[self.df_train['variant'] == variant][self.controls]
            X = self.df_train[self.df_train['variant'] == variant][self.key_features_y]
            
            y = self.df_train[self.df_train['variant'] == variant][self.outcome]
            if self.incentive_var is not None:
                y_incentive = self.df_train[self.df_train['variant'] == variant][self.incentive_var]
                X_incentives = self.df_train[self.df_train['variant'] == variant][self.controls]
            #use model with best parameters
            print(f'best parameters for {variant}', best_params)
            if self.base_model_type == 'xgboost':
                self.hat_models[variant] = clone(XGBRegressor(**best_params))
                if self.incentive_var is not None:
                    self.hat_models[str(variant) + '_incentive'] = clone(RandomizedSearchCV(estimator=model, param_distributions=param_grid,
                                      n_iter=20, cv=5, scoring='neg_mean_squared_error',
                                      n_jobs=-1, random_state=42))
               
            elif self.base_model_type == 'random_forest':
                self.hat_models[variant] = clone(RandomForestRegressor(**best_params))
                if self.incentive_var is not None:
                    self.hat_models[str(variant) + '_incentive'] = clone(RandomizedSearchCV(estimator=model, param_distributions=param_grid,
                                      n_iter=20, cv=5, scoring='neg_mean_squared_error',
                                      n_jobs=-1, random_state=42))
                
            
            self.hat_models[variant].fit(X, y)
            if self.incentive_var is not None:
                
                self.hat_models[str(variant) + '_incentive'].fit(X_incentives, y_incentive)
            
            
        self._predict_ite()
        #find best hyperparameters for variant_0
        for variant_n in range(len(self.treat_mapping['Initial treatment values'])):
             
            new_variant = self.treat_mapping['New treatment variables'][variant_n]
            variant = self.treat_mapping['Initial treatment values'][variant_n]
            X = self.df_test[(self.df_test['variant'] == variant)|
                                (self.df_test['variant'] == 'control') ][self.heterogeneity_dims]    
            y = self.df_test[(self.df_test['variant'] == variant)|
                                (self.df_test['variant'] == 'control') ]['score_'+ new_variant]
           
            strongest_signals = self._get_top_n_features(X, y)
            self.strongest_signals[variant] = strongest_signals
       
        # Fit the models    

    def _predict_ite(self):
        """
        Predict the Individual Treatment Effect (ITE) for each sample in X.

        Parameters:
        - X: New data (features).

        Returns:
        - ite: Estimated Individual Treatment Effect (ITE) for each sample.
        """
        # Predict outcomes for the control group
        self.df_test['control_hat'] = self.hat_models['control'].predict(self.df_test[self.key_features_y])
        
        # Predict outcomes for the treated group
        for variant_n in range(len(self.treat_mapping['New treatment variables'])):
           new_variant = self.treat_mapping['New treatment variables'][variant_n]
           variant = self.treat_mapping['Initial treatment values'][variant_n]
           self.df_test[new_variant + '_hat'] = self.hat_models[variant].predict(self.df_test[self.key_features_y])
           #create a score 'aka' individual treatment effect
           self.df_test['score_'+ new_variant] = ((self.df_test[self.outcome] - self.df_test['control_hat']) * np.where(self.df_test['variant'] == variant,1,0) +
                                         (self.df_test[new_variant + '_hat'] - self.df_test[self.outcome]) * np.where(self.df_test['variant'] == 'control',1,0)+
                                         (self.df_test[new_variant + '_hat'] - self.df_test['control_hat']) * (1 - np.where(self.df_test['variant'] == 'control',1,0) 
                                                                                                 -np.where(self.df_test['variant'] == variant,1,0)))
           if self.incentive_var is not None:
                predict_incentive = self.hat_models[str(variant) + '_incentive'].predict(self.df_test[self.controls])
                self.df_test['score_'+ new_variant] = self.df_test['score_'+ new_variant]/np.where(predict_incentive>np.quantile(predict_incentive, 0.05), predict_incentive, np.quantile(predict_incentive, 0.05))
           #predict score

           self.df_test['score_'+ new_variant +'_hat'] = self.df_test[new_variant + '_hat'] - self.df_test['control_hat']
           if self.incentive_var is not None:
                self.df_test['score_'+ new_variant +'_hat'] = self.df_test['score_'+ new_variant +'_hat']/np.where(predict_incentive>np.quantile(predict_incentive, 0.05), predict_incentive, np.quantile(predict_incentive, 0.05))
           #self.df_test['score_'+ new_variant +'_hat_rank'] = pd.qcut(self.df_test['score_'+ new_variant +'_hat'], q=10, labels=False, duplicates='drop')
   
    def _treatment_for_clusters(self, subsets_dict, outcome_var, variant_col, control_value, treatment_value, covariates=None):
        """
        Computes the treatment effect using OLS regression without formulae for each subset in the provided dictionary.
        Returns a dictionary with the treatment effects and 95% confidence intervals.
    
        Parameters:
        - subsets_dict: Dictionary with descriptive keys and DataFrame subsets as values.
        - outcome_var: The outcome variable (dependent variable).
        - variant_col: The column name for the variant (independent variable of interest).
        - control_value: The control group value in the variant column.
        - treatment_value: The treatment group value in the variant column.
        - covariates: Optional list of covariate column names to include in the model.
    
        Returns:
        - A dictionary with subset descriptions as keys and treatment effects and confidence intervals as values.
        """
        results = {}
        
        for key, subset in subsets_dict.items():
        # Filter subset for control and treatment groups
            
            if not isinstance(subset, pd.DataFrame):
              print(f"Notification: Expected a DataFrame for subset with key '{key}', but got {type(subset)}. Skipping this iteration.")
              print(subset)
              continue  # Skip the rest of this loop iteration

            relevant_data = subset[(subset[variant_col] == control_value) | (subset[variant_col] == treatment_value)].copy()

            
        
        # Create a dummy variable for treatment
            relevant_data.loc[:, 'treatment'] = (relevant_data[variant_col] == treatment_value).astype(int)

             
            base = np.mean(relevant_data[relevant_data['treatment']==0][outcome_var])
        # Prepare the X matrix for OLS
            X = relevant_data[['treatment']]
        
        # Include covariates if provided
            if covariates:
                X = pd.concat([X, relevant_data[covariates]], axis=1)
        
        # Add a constant to the model for the intercept
            X = sm.add_constant(X)
        
        # Prepare the Y vector
            Y = relevant_data[outcome_var]
            #if there are nan  in X drop those columns and print them
            if X.isnull().sum().sum() > 0:
                print('dropping nan columns', X.columns[X.isnull().sum() > 0])
                X = X.dropna(axis=1)
            
            # Fit the OLS model
           
            model = sm.OLS(Y.astype(float), X.astype(float)).fit()
        
        # Extract the treatment effect and confidence intervals
           
            treatment_coef = model.params['treatment']
            #treatment_coef = treatment_coef/base*100
            conf_int = model.conf_int().loc['treatment'].tolist()
            p_value = model.pvalues['treatment']
            #conf_int = np.array(conf_int)/base*100
            if self.incentive_var is not None:
                incentive_mean = np.mean(relevant_data[self.incentive_var])
        # Store the treatment effect and confidence intervals in the results dictionary
                results[key] = {'Treatment Effect': treatment_coef/incentive_mean, '95% Confidence Interval': conf_int/incentive_mean, 'N in anslysis' : len(Y), 'Base': np.nan,  'p_value': p_value, 'N subset': len(subset)}
            else:
                results[key] = {'Treatment Effect': treatment_coef, '95% Confidence Interval': conf_int, 'N in anslysis' : len(Y), 'Base': base, 'p_value': p_value, 'N subset': len(subset)}
    
        return results  
    def fit(self):
        for variant_n in range(len(self.treat_mapping['New treatment variables'])):
            new_variant = self.treat_mapping['New treatment variables'][variant_n]
            variant = self.treat_mapping['Initial treatment values'][variant_n]
            
            subsets = self.all_clusters[variant]
            # Compute the treatment effect for each cluster
            treatment_effects = self._treatment_for_clusters(subsets, self.outcome, 'variant', 'control', variant, self.short_controls)
            # Store the treatment effects
            self.clusters_effect[variant] = treatment_effects
    def plot_treatment_effects(self):
  
    # Check if there are any variants to plot
      if not self.clusters_effect:
          print("No treatment effects computed for any variants.")
          return
    
    # Iterate over each variant and create a plot
      for variant in self.clusters_effect:
          treatment_effects = self.clusters_effect[variant]
        
        # Sort the labels (keys) to ensure segment 0 is the first after sorting
          sorted_labels = sorted(treatment_effects.keys())
        
        # Prepare the data for plotting based on sorted labels
          indices = np.arange(len(sorted_labels))  # Numerical indices for x-axis
          effects = [treatment_effects[key]['Treatment Effect'] for key in sorted_labels]
          lower_bounds = [treatment_effects[key]['95% Confidence Interval'][0] for key in sorted_labels]
          upper_bounds = [treatment_effects[key]['95% Confidence Interval'][1] for key in sorted_labels]

        # Calculate errors for plotting confidence intervals
          errors = [(upper - lower)/2 for upper, lower in zip(upper_bounds, lower_bounds)]

        # Determine bar colors based on statistical significance
          colors = []
          for i, effect in enumerate(effects):
              if lower_bounds[i] > 0:  # Stat. sig. positive
                  colors.append('green')
              elif upper_bounds[i] < 0:  # Stat. sig. negative
                  colors.append('red')
              else:  # Non-significant
                  colors.append('gray')
        
        # Plotting
          fig, ax = plt.subplots(figsize=(10, 5))
          ax.bar(indices, effects, yerr=errors, color=colors, capsize=5, align='center')
          ax.axhline(0, color='black', linewidth=1)  # Draw a line at zero for no effect
          ax.set_xlabel('Segment Index')
          ax.set_ylabel('Treatment Effect')
          ax.set_title(f'Treatment Effect by Segment for {variant}')
          ax.set_xticks(indices)
          ax.set_xticklabels(indices, rotation=45)
          plt.tight_layout()
          plt.show()

        # Creating DataFrame to display segments and their descriptions
          segment_descriptions = pd.DataFrame({
              'Segment Index': indices,
              'Segment Name': sorted_labels
          })

          print(f"Segment descriptions for {variant}:")
        
          for i in indices:
              print(f"Segment {i}: {sorted_labels[i]}")
    def predict_segments(self):
        """
        Uses RuleBasedDecisionTreeRegressor to create data segments based on the decision tree analysis.
        """
        self.dt_models = {}
        for variant_n in range(len(self.treat_mapping['New treatment variables'])):
            new_variant = self.treat_mapping['New treatment variables'][variant_n]
            variant = self.treat_mapping['Initial treatment values'][variant_n]
            self.all_clusters[variant] = {}

            # Prepare the data
            y = self.df_test['score_' + new_variant]
            X = self.df_test[self.strongest_signals[variant]]

            # Create and fit the RuleBasedDecisionTreeRegressor
            dt = UserSegmentor(max_depth=self.n_clusters, 
                                                min_samples_leaf=len(y) // self.n_clusters)
            self.dt_models[variant] = clone(dt)
            self.dt_models[variant].fit(X, y)

            # Predict segments for the estimation set
            X_test = self.df_estimation[self.strongest_signals[variant]]
            self.df_estimation['segment_' + new_variant] = self.dt_models[variant].predict(X_test, return_rules=True)

            # Store data for each segment
            for segment in self.df_estimation['segment_' + new_variant].unique():
                print(segment)
                self.all_clusters[variant][segment] = self.df_estimation[self.df_estimation['segment_' + new_variant] == segment]
              