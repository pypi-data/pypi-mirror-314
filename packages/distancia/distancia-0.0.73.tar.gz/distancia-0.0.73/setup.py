import setuptools
#from setuptools import setup, Extension,find_packages

from distutils.core import setup, Extension

from Cython.Build import cythonize
from readme_renderer import markdown
#ext_modules = cythonize([Extension("distancia.distance", ["distancia/distance.py"])])

with open("README.md", "r") as fh:
    long_description = fh.read()
#with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#    long_description = f.read()    
 

setuptools.setup(
#setup(
    
    #ext_modules=ext_modules,
    #ext_modules = cythonize(ext_modules),


    name="distancia", # Replace with your username

    version="0.0.73",

    author="Yves Mercadier",

    author_email="",

    description="distance metrics,data-science deep-learning machine-learning neural-network",

    long_description=markdown.render(long_description),
    #long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://pypi.org/project/distancia/",

    packages=setuptools.find_packages(),

    classifiers=[

        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

    ],

    python_requires='>=3.0',
    install_requires=[
        # Dépendances minimales nécessaires pour fonctionner
    ],
    extras_require={
        # Dépendance optionnelle pour les fonctionnalités avancées
        "pandas": ["pandas>=1.0.0"],
        "numpy": ["numpy>=1.21.0"],
        "matplotlib": ["matplotlib>=3.5.0"],
        "seaborn": ["seaborn>=0.11.0"],
        "scipy": ["scipy>=1.7.0"],
        "sklearn": ["scikit-learn>=1.0.0"],
        "flask": ["flask>=2.0.0"],
        "networkx": ["networkx>=2.0"],
        "pillow": ["pillow>=8.0.0"],
        "opencv": ["opencv-python>=4.0.0"],
        "requests": ["requests>=2.0.0"],
        "gensim": ["gensim>=4.0.0"],  
        "transformers": ["transformers>=4.0.0"], 
        "torch": ["torch>=1.9.0"],  


        "all": [
            "pandas>=1.0.0",
            "numpy>=1.21.0",
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
            "scipy>=1.7.0",
            "scikit-learn>=1.0.0",
            "flask>=2.0.0",
            "networkx>=2.0",
            "pillow>=8.0.0",
            "opencv-python>=4.0.0",
            "requests>=2.0.0",
            "gensim>=4.0.0",
            "transformers>=4.0.0",
            "torch>=1.9.0"
        ],
    },

)
