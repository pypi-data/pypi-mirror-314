from setuptools import setup, find_packages

setup(
    name='xl_yolo_pkg',  # 这是你包的名字
    version='0.1.0',  # 版本号
    description='A custom SPDConv + WTConv module for YOLO models',  # 包的描述
    long_description = open('README.md', encoding='utf-8').read(),  # 从 README.md 读取长描述
    long_description_content_type='text/markdown',  # 长描述的格式
    author='Zhang XiaoLong',  # 你的名字
    author_email='zhangxl2129@163.com',  # 你的邮箱
    url='https://github.com/zhangxl2129/ultralytics-main',  # 你的项目链接（GitHub 或其他）
    packages=find_packages(),  # 自动找到包
    install_requires=[  # 依赖的库
        'torch',  # 你的包依赖 PyTorch
        # 你可能还需要其它依赖项，比如 numpy
    ],
    classifiers=[  # 分类器，帮助用户找到你的包
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # 如果你使用 MIT 许可证
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # 支持的 Python 版本
)
