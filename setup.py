from setuptools import setup, find_packages


setup_args = dict(
    name='ma-nish',
    version='1.0',
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

with open('requirements.in', 'r', encoding='utf-8') as file:

    install_requires = file.readlines()

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)