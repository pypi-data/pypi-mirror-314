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
    # Simulate heterogeneous treatment effects and add a noise variable
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
    learner = TreatmentEffectLearner(df=data, outcome='y', controls=['x1', 'x2', 'x3'], heterogeneity_dims=['x1'], n_clusters=3)
    learner.get_signals()
    segmentor = UserSegmentor(max_depth=3, min_samples_leaf=10)
    data['segments'] = segmentor.predict(data[['x1', 'x2', 'x3']], return_rules=False)
    assert data['segments'].nunique() <= 3  # Ensures segmentation into a limited number of groups

# Optionally, add additional tests to ensure edge cases and failure modes are handled.

if __name__ == "__main__":
    pytest.main()
