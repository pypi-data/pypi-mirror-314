# Import required functions
from setuptools import setup, find_packages
# from BoBaFor import  _program
_program = "BoBaFor"
# Call setup function
setup(
    author="Paul Phillips",
    description="A machine learning approach for conducting genome wide association studies (GWAS) on bacteria",
    name="BoBaFor",
    packages=find_packages(include=["BoBaFor", "BoBaFor.*", "BoBaFor.Snakefile"]),
    version="0.0.1",
    package_data={'BoBaFor': ['Snakefile', 'GWAS.yml', 'BoBaFor.yml']},
    install_requires=['pandas', 'scipy', 'statsmodels','numpy==1.23.5', 'scikit-learn', 'xgboost', 'matplotlib',  'snakemake', 'Boruta', 'shap', 'seaborn','plotnine', 'pytest'], #'joblib',
    # py_modules=['Snakefile', 'ClassIndexing.py'],
    url="https://github.com/PaulDanPhillips/BoBaFor",
    license="MIT",
    entry_points="""
    [console_scripts]
    {program} = BoBaFor.main:main
    """.format(program=_program),
    include_package_data=True,
)