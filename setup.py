from setuptools import setup, find_packages
from pathlib import Path


with open("README.md", "r", encoding="UTF-8") as f:
     readme = f.read()


setup_args = dict(
    name='ma-nish',
    version='0.9.0',
    description='manish is an unofficial python wrapper for Whatsapp cloud api',
    long_description_content_type="text/markdown",
    long_description=readme,
    license='MIT',
    packages=find_packages(),
    author='Tomer Klein',
    author_email='tomer.klein@gmail.com',
    keywords=['meta', 'ma-nish', 'facebook','whatsapp'],
    url='https://github.com/t0mer/ma-nish',
    download_url='https://pypi.org/project/ma-nish/',
    project_urls={
        "Documentation": "https://github.com/t0mer/ma-nish",
        "Source": "https://github.com/t0mer/ma-nish",
    },
)



install_requires = [
    'python-dotenv',
    'requests',
    'requests-toolbelt',
    'validators',
    'geopy',
    'Pillow',
    'loguru',
    'uvicorn',
    'fastapi',
    'jinja2',
    'dataclasses-json',
    ]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)