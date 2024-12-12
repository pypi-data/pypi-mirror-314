from setuptools import setup, find_packages # 导入setuptools打包工具

setup(
    name='piper_sdk',
    version='0.0.9',    # 包版本号，便于维护版本
    packages=find_packages(include=['piper_sdk', 'piper_sdk.*']),
    include_package_data=True,
    install_requires=[
        'python-can>=4.3.1',
    ],
    entry_points={
    },
    author='RosenYin',  # 作者
    author_email='yinruocheng321@gmail.com',
    description='A sdk to control piper',   #包的简述
    # url="https://github.com/agilexrobotics/piper_sdk",
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    # python_requires='>=3.8',    #对python的最低版本要求
)

