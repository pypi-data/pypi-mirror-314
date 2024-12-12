from setuptools import setup, find_packages

setup(
    name="planetra_solver",
    version="0.1.4",
    description="The library contains basic functions that can help in Planetra development",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Anton Vyugin, Ruslan Gafurov",
    author_email="anton.vyugin.00@mail.ru, g.r.9@mail.ru",
    url="https://planetra.gitlab.yandexcloud.net/testgroup/planetra_solver.git",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
