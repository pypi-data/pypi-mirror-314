from setuptools import setup, find_packages

setup(
    name="shareithub",  # Nama unik paket Anda
    version="0.7.0",  # Versi paket
    author="SHARE IT HUB",
    author_email="yt.shareithub@gmail.com",
    description="Dont forget Subscribe",
    long_description=open("README.md").read(),  # Isi dari README.md
    long_description_content_type="text/markdown",
    url="https://github.com/shareithub?tab=repositories",  # URL repositori atau proyek Anda
    packages=find_packages(),  # Secara otomatis menemukan submodul
    install_requires=[
        "requests",
        "aiohttp",
        "colorama",
        "beautifulsoup4",  # BeautifulSoup4 -> BeautifulSoup4 seharusnya ditulis dengan huruf kecil
        "asyncio",
        "schedule",
        "pyautogui",
        "cryptography",
        "pycryptodome",
        "loguru",
        "logging",
        "datetime",
        "pytz",
        "python-telegram-bot",
        "telethon",
        "fake-useragent",
    ],  # Dependensi yang dibutuhkan
    include_package_data=True, 
    package_data={  
        'shareithub': [
            'ascii_tools.py',
            'http_tools.py',
            '__init__.py'
        ],  # Menyertakan beberapa file dalam folder shareithub
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Versi Python minimal
)
