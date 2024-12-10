from distutils.core import setup
# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='wordlyzer3',  # Nama package yang sesuai dengan folder project
    packages=['wordlyzer3'],  # Nama folder yang sama dengan 'name'
    version='0.3',  # Versi pertama dari library
    license='MIT',  # Lisensi yang digunakan
    description='A simple library for text analysis',  # Deskripsi singkat tentang library
    long_description=long_description,  # Deskripsi panjang dari README.md
    long_description_content_type='text/markdown',
    author='Nurico Vicyyanto',  # Nama Anda
    author_email='nuricovicyyanto@gmail.com',  # Email Anda
    url='https://github.com/NuricoVicyyanto/wordlyzer.git',  # Ganti dengan URL GitHub Anda
    download_url='https://github.com/nuricovicyyanto/wordlyzer/archive/v_01.tar.gz',  # Link untuk mengunduh versi 0.1
    project_urls={
        'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/nuricovicyyanto',
        'Source': 'https://github.com/nuricovicyyanto/wordlyzer',
        'Tracker': 'https://github.com/nuricovicyyanto/wordlyzer/issues',
    },
    keywords=['text', 'analysis', 'python', 'library'],  # Kata kunci yang mendeskripsikan library
    install_requires=[  # Daftar dependensi yang diperlukan
        'validators',
        'beautifulsoup4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Status pengembangan
        'Intended Audience :: Developers',  # Target audiens: Developer
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',  # Lisensi yang digunakan
        'Programming Language :: Python :: 3',  # Mendukung Python 3
        'Programming Language :: Python :: 3.7',  # Mendukung Python 3.7
        'Programming Language :: Python :: 3.8',  # Mendukung Python 3.8
        'Programming Language :: Python :: 3.9',  # Mendukung Python 3.9
        'Programming Language :: Python :: 3.10',  # Mendukung Python 3.10
        'Programming Language :: Python :: 3.11',  # Mendukung Python 3.11
    ],
)
