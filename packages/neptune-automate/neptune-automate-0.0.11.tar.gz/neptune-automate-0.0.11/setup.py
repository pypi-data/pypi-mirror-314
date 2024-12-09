from setuptools import setup, find_packages

setup(
    name="neptune-automate",
    version="0.0.11",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "statsmodels", 
        "scikit-learn", 
        "xgboost", 
        "lightgbm", 
        "catboost", 
        "numpy", 
        "pandas", 
        "twine", 
        "setuptools"
    ],
)




