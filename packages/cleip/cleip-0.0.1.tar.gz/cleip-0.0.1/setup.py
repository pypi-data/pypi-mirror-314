from setuptools import setup, find_packages

setup(
    name='cleip',
    version='0.0.1',
    author='Tobias Herrmann',
    author_email='tobias@cleip.com',
    description='Cleip Python SDK',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://cleip.com',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)