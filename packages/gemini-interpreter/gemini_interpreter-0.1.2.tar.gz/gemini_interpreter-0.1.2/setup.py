from setuptools import setup, find_packages

setup(
    name="gemini-interpreter",
    version="0.1.2",
    description="AI interpreter project",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Illya Lazarev",
    author_email="sbdt.israel@gmail.com",
    url="https://github.com/Python-shik/gemini-interpreter",
    install_requires=[
        "requests",
        "psutil"
    ],
    packages=find_packages(where="src"),  # Автоматический поиск пакетов в директории `src`
    package_dir={"": "src"},  # Указываем, что корень пакетов в папке `src`
    entry_points={
        "console_scripts": [
            "ai-chat=main",  # Связываем консольную команду с функцией `main` в `main.py`
        ]
    },
    include_package_data=True,  # Включает дополнительные файлы в пакеты
    package_data={
        "": ["conversations/*"],  # Указываем, что нужно добавить файлы из папки conversations
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
