from setuptools import setup, find_packages

setup(
    name="yuya-py",
    version="1.1.0",  # VERSÃO ESTÁVEL NOVA
    packages=find_packages(),
    install_requires=[
        "PyQt5",
        "opencv-python",
        "numpy",
    ],
    author="Thiaguin",
    description="A LIB MAIS BRABA DE INTERFACE GRÁFICA! 🔥",
    long_description="""Interface gráfica STYLE em Python, feita por uma criança que programa python (no caso eu).

VERSÃO ESTÁVEL 1.1.0 - MAIS BRABA AINDA! 🔥

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