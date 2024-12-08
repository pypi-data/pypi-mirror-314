from setuptools import setup, find_packages
from setuptools.command.install import install
import nltk

class PostInstallCommand(install):
    """Post-installation for installing NLTK resources."""

    def run(self):
        install.run(self)
        resources = [
            "averaged_perceptron_tagger_eng",
            "wordnet",
            "stopwords",
            "punkt_tab",
        ]
        for resource in resources:
            try:
                nltk.download(resource, quiet=True)
            except Exception as e:
                print(f"Failed to download resource {resource}: {e}")


setup(
    name="TPTK",
    version="0.0.9",
    author="Gaurav Jaiswal",
    author_email="jaiswalgaurav863@gmail.com",
    description="Automate text preprocessing tasks with ease.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Gaurav-Jaiswal-1/Text-Preprocessing-Toolkit",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "nltk>=3.6.0",
        "pyspellchecker>=0.7.1",
        "pandas>=1.2.0",
    ],
    python_requires=">=3.8",
    cmdclass={
        'install': PostInstallCommand,
    },
)
