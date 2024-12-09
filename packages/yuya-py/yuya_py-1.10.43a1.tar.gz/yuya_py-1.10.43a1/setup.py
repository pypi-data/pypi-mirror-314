from setuptools import setup, find_packages

setup(
    name="yuya-py",
    version="1.10.43a1",  
    packages=find_packages(),
    install_requires=[
        "PyQt5",
        "opencv-python",
        "numpy",
    ],
    author="Thiaguin",
    description="A LIB MAIS BRABA DE INTERFACE GRÁFICA! 🔥",
    long_description="""Interface gráfica STYLE em Python, feita por uma criança que programa python (no caso eu).

Como usar:
from yuya_py import YuyaPy

Features:
- Interface STYLE
- Gradientes BRABO
- Animações SINISTRAS
""",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)