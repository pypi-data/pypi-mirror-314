from setuptools import setup, find_packages

setup(
    name='sophy-python',  # This is the name that will be used with pip install
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Sidhart Krishnan',
    author_email='sidhartkrishnan@gmail.com',
    description='A Slack notification utility',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SidhartK/sophy-python',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)