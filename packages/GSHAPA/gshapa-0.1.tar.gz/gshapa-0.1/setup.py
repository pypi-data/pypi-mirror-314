import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gshapa",
    version="0.0.1",
    author="Sara Khademioureh, Irina Dinu, Sergio Peignier",
    description="Gene Set Analysis for Single-Cell RNA-seq Using Random Forest and SHAP Values",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'tqdm',
        'scipy',
        'statsmodels',
        'fasttreeshap',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
)

print(setuptools.find_packages())
