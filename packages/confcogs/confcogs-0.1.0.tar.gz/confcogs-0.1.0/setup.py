from setuptools import setup, find_packages

setup(
    name='confcogs',
    version='0.1.0',
    description='Lib for managing .cogs file',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='pathset',
    author_email='abyzmsamphetamine@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    python_requires='>=3.6',
)
