import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tools-zy",
    version="0.1.7.2", # 每次上传,需要更改版本号
    author="Zhiyuan Wang",
    author_email="WangZhiyuan@mail.ustc.edu.cn",
    description="Some tools for AI model training and inference.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wzy-777/tools_zy",
    packages=setuptools.find_packages(),
    install_requires=[
        # 'Pillow>=5.1.0', 
        'numpy>=1.14.4',
        'tqdm>=4.0.0'
        ], # 依赖的库
    entry_points={
        # 'console_scripts': [
        #     'example=tools_zy.example:main'
        # ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    python_requires='>=3.10',
)