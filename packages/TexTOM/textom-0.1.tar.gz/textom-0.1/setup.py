from setuptools import setup, find_packages

setup(
    name="TexTOM",          
    version="0.1",       
    author="Moritz Frewein, Marc Allain, Tilman Gruenewald",
    author_email="textom@fresnel.fr",
    description="A program for texture simulations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.fresnel.fr/textom/textom.git", 
    packages=find_packages(), 
    include_package_data=True,
    package_data={
        "textom": [
        "ressources/symmetrizedHSH/output/*",
        "ressources/*.txt",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9, <=3.12',
    install_requires=["mumott", "pyfai", "orix", "ipython"],
    entry_points={
        "console_scripts": [
            "textom=textom.textom:main",
        ]
    },
)