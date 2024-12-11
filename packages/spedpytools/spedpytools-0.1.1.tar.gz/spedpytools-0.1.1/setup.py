from setuptools import setup
from setuptools import find_packages

from spedpytools import __version__

def parse_requirements(filename):
    with open(filename, encoding='utf-16') as f:
        return f.read().splitlines()

setup(name='spedpytools',
    version=__version__,
    license='MIT License',
    author='Ismael Nascimento',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author_email='ismaelnjr@icloud.com.br',
    keywords='sped fiscal receita federal',
    description=u'Biblioteca para visualização de um arquivo sped em estrutura de tabelas do Pandas e possibilidade de salvar em formato para excel.',
    packages=find_packages(),
    include_package_data=True,
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

