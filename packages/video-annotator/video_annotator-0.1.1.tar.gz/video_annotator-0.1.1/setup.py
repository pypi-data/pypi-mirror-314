from setuptools import setup, find_packages

setup(
    name='video-annotator',  # Nama paket yang akan digunakan dengan pip install
    version='0.1.1',  # Versi pertama dari paket
    description='A Python package for video annotation, object tracking, and cropping',  # Deskripsi singkat
    long_description=open('README.md').read(),  # Membaca README sebagai deskripsi panjang
    long_description_content_type='text/markdown',  # Format deskripsi panjang
    author="Moh. Jeli Almuta'ali",  # Ganti dengan nama Anda
    author_email='jelimutaalidev@gmail.com',  # Ganti dengan email Anda
    url='https://github.com/jelimutaalidev/video-annotator',  # Ganti dengan URL repositori GitHub Anda
    packages=find_packages(),  # Secara otomatis menemukan semua sub-package
    install_requires=[  # Daftar dependensi eksternal yang diperlukan oleh paket Anda
        'supervision>=0.1.1',
        'tqdm>=4.50.0',
    ],
    classifiers=[  # Menambahkan classifier untuk membantu orang lain menemukan paket Anda
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Tentukan versi Python yang kompatibel
)
