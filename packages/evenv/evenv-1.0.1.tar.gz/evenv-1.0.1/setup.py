from setuptools import setup, find_packages

setup(
    name="evenv",
    version="1.0.1",
    author="artemdorozhkin",
    author_email="aa.dorozhkin@ya.ru",
    description="Creates virtual embeddable Python "
        "environments in one or "
        "more target "
        "directories.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/artemdorozhkin/evenv",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    package_data={
        "": ["bundled/*.zip"],
    },
    include_package_data=True, 
)
