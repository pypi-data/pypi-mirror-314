import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="pennylane-cim",
    version="0.0.1",
    author="Quanta",
    author_email="Quanta@",
    description="A plugin connect pennlylane and cim.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/hpcl_quanta/pennylane-cim-plugin",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        'pennylane',
    ],
    python_requires=">=3.12",
)