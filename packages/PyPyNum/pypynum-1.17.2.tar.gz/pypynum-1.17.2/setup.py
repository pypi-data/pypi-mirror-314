from setuptools import setup, find_packages

with open("pypynum/README.md", "r", encoding="UTF-8") as r:
    md = r.read()

keywords = [
    "math", "数学", "mathematics", "数学计算", "numerical", "数值", "computation", "计算",
    "scientific", "科学", "algebra", "代数", "calculus", "微积分", "statistics", "统计",
    "linear-algebra", "线性代数", "optimization", "优化", "numerical-analysis", "数值分析", "matrix", "矩阵",
    "vector", "向量", "tensor", "张量", "numerics", "数值计算", "library", "库",
    "tools", "工具", "utils", "实用程序", "algorithms", "算法", "software", "软件",
    "package", "包", "methods", "方法", "data-science", "数据科学", "machine-learning", "机器学习",
    "computational", "计算的", "operations", "操作", "functions", "函数", "processing", "处理",
    "programming", "编程", "simulation", "仿真", "visualization", "可视化", "physics", "物理"
]

with open("AGPLv3", "r", encoding="UTF-8") as r:
    LICENSE = r.read()

setup(
    name="PyPyNum",
    version="1.17.2",
    packages=find_packages(),
    url="https://github.com/PythonSJL/PyPyNum",
    license=LICENSE,
    author="Shen Jiayi",
    author_email="2261748025@qq.com",
    description="PyPyNum is a multifunctional Python math lib. It includes modules for math, data analysis, array ops, "
                "crypto, physics, randomness, data prep, stats, solving eqns, image processing, interp, matrix calc, "
                "and high-precision math. Designed for scientific computing, data science, and machine learning, "
                "PyPyNum provides efficient and versatile tools.",
    python_requires=">=3.4",
    package_data={"pypynum": ["*"]},
    long_description=md,
    long_description_content_type="text/markdown",
    keywords=keywords
)
