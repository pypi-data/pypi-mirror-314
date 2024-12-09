# test_uplift_segmentation.py

import pytest
import pandas as pd
import numpy as np
from UpliftSegmentation.treatment_effect_learner import TreatmentEffectLearner
from UpliftSegmentation.user_segmentor import UserSegmentor

def generate_data(n=1000):
    np.random.seed(42)
    data = pd.DataFrame({
        'x1': np.random.normal(0, 1, n),
        'x2': np.random.normal(0, 1, n),
        'x3': np.random.normal(0, 1, n),
        'T': np.random.binomial(1, 0.5, n)  # 50% treatment probability
    })
    # Simulate heterogeneous treatment effects
    data['y'] = 2 + data['x1'] + 2 * data['x2'] - 1.5 * data['x3'] + data['T'] * (data['x1'] * 0.5 + 2) + np.random.normal(0, 0.5, n)
    data['variant'] = data['T']
    return data

def test_treatment_effect_learner_initialization():
    data = generate_data(100)
    learner = TreatmentEffectLearner(df=data, outcome='y', controls=['x1', 'x2', 'x3'], heterogeneity_dims=['x1'], n_clusters=5)
    assert learner.df is not None
    assert learner.outcome == 'y'
    assert 'x1' in learner.controls

def test_treatment_effect_learner_calculation():
    data = generate_data(200)
    learner = TreatmentEffectLearner(df=data, outcome='y', controls=['x1', 'x2', 'x3'], heterogeneity_dims=['x1'], n_clusters=5)
    learner.get_signals()
    assert 'control' in learner.hat_models

def test_user_segmentor_integration():
    data = generate_data(300)
    learner = TreatmentEffectLearner(df=data, outcome='y', controls=['x1', 'x2', 'x3'], heterogeneity_dims=['x1', 'x2'], n_clusters=3)
    learner.get_signals()
    learner.predict_segments()
    #segmentor = UserSegmentor(max_depth=3, min_samples_leaf=10)
    # Ensure the UserSegmentor is applied correctly
    #data['segments'] = segmentor.predict(data[['x1', 'x2', 'x3']], return_rules=False)
    assert learner.df_estimation['segment_variant_0'].nunique() <= 3  # Ensures segmentation into a limited number of groups

def test_predict_segments():
    from UpliftSegmentation.user_segmentor import UserSegmentor
    data = generate_data(500)
    learner = TreatmentEffectLearner(df=data, outcome='y', controls=['x1', 'x2', 'x3'], heterogeneity_dims=['x1', 'x2'], n_clusters=4)
    learner.get_signals()
    learner.predict_segments()
    # Ensures that segments are created and stored correctly
    assert 'segment_variant_0' in learner.df_estimation.columns
    num_segments = learner.df_estimation['segment_variant_0'].nunique()
    assert num_segments <= 4  # Should not exceed the number of clusters specified

# Optionally, you can add a command line interface for running pytest directly
if __name__ == "__main__":
    pytest.main()
