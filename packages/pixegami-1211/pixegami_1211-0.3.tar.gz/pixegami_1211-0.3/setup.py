from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="pixegami_1211",
    version="0.3",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pixegamiii = pixegami_1211:hello",
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
)
