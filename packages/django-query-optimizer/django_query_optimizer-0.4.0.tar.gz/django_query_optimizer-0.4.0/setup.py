from setuptools import setup, find_packages

setup(
    name="django_query_optimizer",
    version="0.4.0",                
    description="Automatic optimization of django queries",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Yasin Karbasi",
    author_email="yasinkardev@gmail.com",
    url="https://github.com/YasinKar/django_query_optimizer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",            
    install_requires=[
        "django"
    ],
)