from pathlib import Path

from setuptools import setup, find_packages

current_dir = Path(__file__).parent
long_description = (current_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="NTkpp",
    version="0.0.3.2",
    author="Тихонов Иван",
    author_email="tihonovivan737@gmail.com",
    description="Простая библиотека для полносвязных нейронных сетей",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "numpy",
    ],
)
