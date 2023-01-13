from setuptools import setup, find_packages


setup_args = dict(
    name='ma-nish',
    version='1.0.0',
    description='ma-nish is an unofficial python wrapper for Whatsapp cloud api',
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    author='Tomer Klein',
    author_email='tomer.klein@gmail.com',
    keywords=['meta', 'ma-nish', 'facebook','whatsapp'],
    url='https://github.com/t0mer/ma-nish',
    download_url='https://pypi.org/project/ma-nish/'
)

install_requires = [
    'python-dotenv>=0.21.0',
    'requests>=2.28.1',
    'requests-toolbelt>=0.10.1',
    'validators>=0.20.0',
    'geopy>=2.3.0',
    'Pillow>=9.3.0',
    'loguru==0.6.0',
    'uvicorn==0.20.0',
    'fastapi==0.88.0',
    'jinja2==1.2 ',
    ]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)