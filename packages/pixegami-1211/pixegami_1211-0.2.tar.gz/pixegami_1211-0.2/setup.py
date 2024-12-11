from setuptools import setup, find_packages

setup(
    name="pixegami_1211",
    version="0.2",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pixegamiii = pixegami_1211:hello",
        ],
    },
)
