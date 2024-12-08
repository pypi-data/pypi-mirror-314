from setuptools import setup, find_packages

setup(
    name="arsls",  # Paket ismi
    version="1.0",  # Versiyon numarası
    description="A simple URL Shortener with GUI made using CustomTkinter.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",  # README'nin Markdown olarak okunması
    author="ArsTech",  # Yazar ismi
    author_email="arstechai@gmail.com",  # E-posta adresin
    url="https://github.com/e500ky/arsls",  # GitHub repo URL'si
    packages=find_packages(),  # Paketleri otomatik bul
    include_package_data=True,  # Ek dosyaları dahil et
    install_requires=[
        "customtkinter",
        "pyshorteners",
        "pyperclip",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",  # Python sürüm gereksinimi
    entry_points={
        "console_scripts": [
            "arsls=arsls.__init__:main",  # Konsol komutu oluşturma
        ],
    },
)
