from setuptools import setup, find_packages

setup(
    name='spotmate',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'spotipy>=2.23.0',
        'pytest>=6.2.5',
        'setuptools>=57.0.0',
    ],
    entry_points={
        'console_scripts': [
            'spotmate=spotmate.main:main',
        ],
    },
    author='Ankit Kumar Ravi',
    description='A CLI tool to manage your Spotify playlists.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/riAssinstAr/Spot-Mate',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
