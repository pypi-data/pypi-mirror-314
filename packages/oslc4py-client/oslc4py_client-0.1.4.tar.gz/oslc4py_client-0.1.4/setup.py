from setuptools import setup, find_packages

setup(
    name="oslc4py_client",
    version="0.1.4",
    author="Matej Grós",
    author_email="492906@mail.muni.cz",
    description="OSLC Python client with common annotation types",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pajda.fit.vutbr.cz/verifit/oslc4py-client",
    packages=[
        "oslc4py_client",
        "oslc4py_client.annotation_types",
    ], 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "rdflib" 
    ],
    python_requires='>=3.6',
)