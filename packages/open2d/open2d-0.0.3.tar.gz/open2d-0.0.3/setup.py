from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

# # 创建 Cython 扩展模块
# extensions = [
#     Extension(
#         "open2d.imagealgorithman",  # 模块名称，注意这里要使用新的路径
#         ["src/open2d/imagealgorithman.py"],  # Cython 文件路径
#     )
# ]

setup(
    name="open2d",
    version="0.0.3",
    description="This is a collection of digital image algorithms.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="AlMan",
    # author_email="your_email@example.com",
    # url="https://github.com/yourusername/my_project",
    # packages=["open2d"],  # 修改为新的包路径
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    ext_modules=cythonize([
        Extension( #指明模块的名称和源代码文件路径
            "open2d.imagealgorithman",  # 模块名称，注意这里要使用新的路径
            ["src/open2d/imagealgorithman.pyx"],  # Cython 文件路径
        )
    ]),  # 使用 cythonize 编译扩展
    # install_requires=["numpy", "opencv-python"],  # 安装依赖
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Cython",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)
