from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='EwanSonicConnector',
    version='0.1.10',
    packages=find_packages(),
    install_requires=[
        'redis==5.0.1',
        'requests==2.31.0',
        'airtest==1.3.5',
    ],
    author='fulage',
    author_email='fulage@ewan.cn',
    description='给ewan内部使用的一个连接云真机sonic的连接器',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
