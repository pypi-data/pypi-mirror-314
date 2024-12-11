from setuptools import setup, find_packages

setup(
    name="unic4py",
    version="0.1.4",
    author="Matej Grós",
    author_email="492906@mail.muni.cz",
    description="OSLC Analyser for Unite",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pajda.fit.vutbr.cz/verifit/unic4py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "oslc4py_client>=0.1.4",
        "oslc4py_domains_auto>=0.1.2" 
    ],
    python_requires='>=3.6',
)