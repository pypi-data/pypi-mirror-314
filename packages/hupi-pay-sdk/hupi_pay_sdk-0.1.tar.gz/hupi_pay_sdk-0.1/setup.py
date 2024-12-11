from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="hupi_pay_sdk",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'certifi',
        'charset-normalizer',
        'idna',
        'requests',
        'urllib3',
    ],
    author="yareta",
    author_email="yareta2324@gmail.com",
    description="A brief description of your package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # 提供一个有效的项目URL
    url="https://github.com/your-username/hupi_pay_sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
