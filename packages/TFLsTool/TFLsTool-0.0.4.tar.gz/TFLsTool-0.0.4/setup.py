# coding:utf-8

from setuptools import setup

with open('ReadMe.md') as f:
    long_description = f.read()


setup(
        name='TFLsTool',
        version='0.0.4',
        description='This is a toolkit related to TFL (Tables, Figures, and Listings) generation in the field of clinical biostatistics for pharmaceuticals.',
        author='allensrj',
        author_email='allensrj@qq.com',
        url='https://github/allensrj/',
        long_description=long_description,
        long_description_content_type='text/markdown',
        license='MIT',
        package_dir={'TFLsTool': 'src'},
        install_requires=[
                'pandas>=2.2.1',
                'numpy>=1.21.0',
                'python-docx==0.8.11',
                'zhon==2.0.2',
                'openpyxl>=3.1.0',
                'matplotlib'
        ]
)