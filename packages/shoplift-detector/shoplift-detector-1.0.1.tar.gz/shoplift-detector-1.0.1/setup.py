from setuptools import setup, find_packages

setup(
    name="shoplift-detector",
    version="1.0.1",
    description="Un système de détection des comportements de vol à partir des images de vidéosurveillance dans les supermarchés.",
    author="donatmat",
    author_email="matendodonat93@gmail.com",
    url="https://github.com/donatmat/shoplift-detector",
    packages=find_packages(),
    include_package_data=True,  # Inclure les fichiers non-Python
    package_data={
        "shoplift_detector": ["models/*.h5"],  # Spécifie les fichiers de modèle
    },
    install_requires=[
        "numpy",
        "opencv-python",
        "tensorflow>=2.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
