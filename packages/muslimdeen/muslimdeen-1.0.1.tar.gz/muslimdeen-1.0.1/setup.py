from setuptools import setup, find_packages

# Lire le README.md pour la description longue
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
required = [
    "numpy==2.2.0",
    "pandas==2.2.3",
    "requests==2.32.3",
    "python-dateutil==2.9.0.post0",
    "pytz==2024.2",
    "sentence-transformers==3.3.1",
    "faiss-cpu==1.9.0.post1",
    "regex==2024.11.6",
    "rapidfuzz==3.10.1",
    "symspellpy==6.7.8",
    "torch==2.5.1",
    "transformers==4.47.0"
]

setup(
    name='muslimdeen',
    version='1.0.1',
    packages=find_packages(),
    install_requires=required,
    description='MuslimDeen: Package pour gérer les sourates et le coran',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="personne monsieur",
    author_email="monsieurnobody01@gmail.com",
    url='https://gitlab.com/misternobody01/package_muslimdeen.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True
)
