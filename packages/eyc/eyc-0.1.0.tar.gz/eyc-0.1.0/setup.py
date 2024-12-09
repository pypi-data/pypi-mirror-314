from setuptools import setup, find_packages

setup(
    name="eyc",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    description="EYC - Türkçe programlama dili",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Adınız",
    author_email="email@ornek.com",
    url="https://github.com/gamesitesi/eyc",  # GitHub Proje URL'si
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
