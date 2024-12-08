from setuptools import setup, Extension
from Cython.Build import cythonize

# 创建 Cython 扩展模块
extensions = [
    Extension(
        "src.imagealgorithman",  # 模块名称
        ["src/imagealgorithman.pyx"],  # Cython 文件路径
    )
]

setup(
    name="open2d",
    version="0.0.0",
    description="This is a collection of digital image algorithms.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="AlMan",
    packages=["src"],
    ext_modules=cythonize(extensions),  # 使用 cythonize 编译扩展
    install_requires=["numpy", "opencv-python"],  # 安装依赖
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Cython",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)
