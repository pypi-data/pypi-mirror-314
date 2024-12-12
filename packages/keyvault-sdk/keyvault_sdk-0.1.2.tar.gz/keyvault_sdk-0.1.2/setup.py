from setuptools import setup, find_packages

setup(
    name='keyvault-sdk',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pycryptodome',
        'apscheduler',
    ],
    author='single.wong',
    author_email='wongsingle@163.com',
    description='密钥管理服务的Python SDK',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7.5',
)
