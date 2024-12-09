from setuptools import setup, find_packages

setup(
    name='Telon',
    version='0.2',
    packages=find_packages(),
    description='A simple Telegram bot library using requests',
    author='Ahmed',
    author_email='a7mednegm.x@example.com',
    url='https://github.com/x7007x/TgMan',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.24.0'
    ],
)