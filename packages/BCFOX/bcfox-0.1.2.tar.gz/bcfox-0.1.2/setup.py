from setuptools import setup, find_packages

setup(
    name="BCFOX",
    version="0.1.2",
    author="Guilherme Neri",
    author_email="guilherme.neri@bcfox.com.br",
    description="Biblioteca BCFOX",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GuilhermNeri/BCFOX",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        'selenium',              # Selenium para automação
        'selenium-stealth',      # Selenium Stealth para ocultar o driver
        'undetected-chromedriver',  # Para usar o Chrome com contorno de proteção
        'requests',              # Para fazer requisições HTTP
    ],
)
