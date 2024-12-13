from setuptools import setup, find_packages

setup(
    name="cheat_chat",
    version="0.3.0",
    author="Abdullah Zeynel & Zeren Kavaz & Kerem Durgut & Mesude Türkmen",
    author_email="your_email@example.com",
    description="A server-client chat application with Redis and MySQL support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MesudeTurkmen/cheat_chat",  # GitHub URL
    packages=find_packages(),
    install_requires=[
        "asyncio"  # veya başka gerekli kütüphaneler
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
