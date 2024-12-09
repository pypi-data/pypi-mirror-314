from setuptools import setup, find_packages

setup(
    name='UpliftSegmentation',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'xgboost',
        'matplotlib'  # If you use it in your classes
    ],
    author='Eddie Baigabulov',
    author_email='eddie.baigabulov@instacart.com',
    description='This is a Python package designed for modeling and analyzing treatment effects to optimize user segmentation and uplift strategies.'
)

