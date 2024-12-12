from setuptools import setup, find_packages

setup(
    name="framework_rizomatico",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "plotly",
        "pyspark"
    ],
    author="Seu Nome",
    description="Framework rizomático com microkernels interativos",
    url="https://github.com/seu-repo/framework_rizomatico",
)
