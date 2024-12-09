from setuptools import setup, find_packages

setup(
    name='LAB_11',
    version='0.1.0',
    author='VeroKulak',
    author_email='nickkol31@gmail.com',
    description='Краткое описание mypackage',
    long_description=open('README.md', encoding = 'utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ваш_репозиторий',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
