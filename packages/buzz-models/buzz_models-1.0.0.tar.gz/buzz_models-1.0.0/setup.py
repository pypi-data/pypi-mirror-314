# shared_models/setup.py
from setuptools import setup, find_packages


# 打包命令 python setup.py sdist bdist_wheel
# pip install twine
# twine upload dist/*
setup(
    name='buzz_models',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'sqlmodel>=0.0.6',
        'sqlalchemy[asyncio]>=1.4'
    ],
    author="mails",
    author_email="s644100298@gmail.com",
    description="buzz的数据库模型",
    url="https://github.com/yourusername/shared_models"
)
