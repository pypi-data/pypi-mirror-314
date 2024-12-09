from setuptools import setup, find_packages
import sys

setup(
    name='MMonitor-Mindspore',
    version='1.0.0',
    license="MIT",
    url="https://openi.pcl.ac.cn/wec/MMonitor",
    description='A Toolkit for understanding the training of neural network',
    classifiers=[
        'Development Status :: 3 - Alpha',
        # 开发的目标用户
        'Intended Audience :: Science/Research',
        # 许可证信息
        'License :: OSI Approved :: MIT License',
        # 目标 Python 版本
        'Programming Language :: Python :: 3.8',
        # 属于什么类型
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    setup_requires=[
    ],
    install_requires=[
        'wandb',
        'plotly',
        'seaborn',
        'transformers',
        'einops',
        'mindspore'
    ],
    packages=find_packages(),
)
