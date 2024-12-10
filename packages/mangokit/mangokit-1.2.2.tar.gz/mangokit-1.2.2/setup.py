from setuptools import setup, find_packages

__version__ = '1.2.2'

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='mangokit',
    version=__version__,
    description='测试工具',
    long_description=long_description,
    package_data={
        'mangokit': [
            'mango.cp310-win_amd64.pyd',
            'mango.cpython-310-x86_64-linux-gnu.so'
        ]
    },
    author='毛鹏',
    author_email='729164035@qq.com',
    url='https://gitee.com/mao-peng/testkit',
    packages=find_packages(),
    install_requires=[
        'jsonpath==0.82.2',
        'requests==2.32.3',
        'aiohttp==3.10.11',
        'aiomysql==0.2.0',
        'PyMySQL==1.1.1',
        'jsonpath==0.82.2',
        'cachetools==5.3.1',
        'Faker==24.1.0',
        'diskcache==5.6.3',
        'urllib3==2.2.3',
        'pydantic==2.9.2',
        'colorlog==6.7.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ]
)

"""


python -m pip install --upgrade setuptools wheel
python -m pip install --upgrade twine

python setup.py check
python setup.py sdist bdist_wheel
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

"""
