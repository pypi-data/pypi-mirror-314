from setuptools import setup, find_packages
import subprocess
import sys
from setuptools.command.install import install

class CustomInstall(install):
    """自定义安装命令"""
    def run(self):
        # 在安装前运行自定义的 install_dependencies 函数
        self.install_dependencies()
        super().run()

    def install_dependencies(self):
        """确保安装外部依赖（samtools 和 minimap2）"""
        print("请确保已安装以下外部工具：")
        print("1. samtools")
        print("2. minimap2")
        print("\n请使用以下命令安装：")
        print("sudo apt-get install samtools minimap2  # 对于 Ubuntu/Debian 系统")
        print("brew install samtools minimap2  # 对于 macOS 系统")

setup(
    name='pypi_test_package',  # 包名
    version='0.1.6',  # 版本号
    # packages=find_packages(),  # 自动找到所有包
    packages=['pypi_test_package'],  # 明确指定包含的包
    install_requires=[],  # 其他 Python 包依赖（这里为空，可以根据需要添加）
    include_package_data=True,  # 包括非 Python 文件（比如 .pyc）
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # 支持的最低 Python 版本
    entry_points={  # 自定义命令行工具
        'console_scripts': [
            'install-dependencies=pypi_test_package.install_dependencies:install_dependencies',  # 添加安装依赖的命令
        ],
    },
    cmdclass={  # 自定义安装步骤
        'install': CustomInstall,  # 使用自定义安装命令
    },
)
