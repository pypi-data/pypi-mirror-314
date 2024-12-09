from setuptools import setup, find_packages

setup(
    name="motorrijtuigenbelasting",
    version="0.1.0",
    description="Calculate Dutch road tax Motorrijtuigenbelasting(MRB) for vehicles.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vito Minheere",
    author_email="vito@vipyr.nl",
    url="https://github.com/VitoMinheere/motorrijtuigenbelasting",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
