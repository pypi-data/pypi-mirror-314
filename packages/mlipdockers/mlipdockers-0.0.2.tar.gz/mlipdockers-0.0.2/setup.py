from setuptools import setup, find_packages

setup(
    name="mlipdockers",
    version="0.0.2",
    author="Yaoshu Xie",
    author_email="jasonxie@sz.tsinghua.edu.cn",
    description="Request to docker containers in which the python enviroments for different machine learning potential usages are implemented. Using this package, one can get the predicted potential energy for any structure using any MLIP without needing to change python environments.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/HouGroup/ys_mlipdk/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[
        "docker",
        
    ]
)
