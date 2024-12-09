from setuptools import setup, find_packages

setup(
    name="visibl_docs",
    version="0.1.7",
    packages=find_packages(exclude=['visibl_docs.dev_tools*']),
    install_requires=[
        "flask==3.0.0",
        "werkzeug==3.0.1",
        "click>=8.0.0",
        "setuptools",
        "requests==2.31.0",
        "psutil==5.9.5",
        "uvicorn==0.24.0",
        "fastapi==0.104.1",
        "python-dotenv>=0.19.0",
        "python-jose[cryptography]>=3.3.0",
        "auth0-python>=4.0.0",
        "keyring>=23.0.0",
        "authlib>=1.0",
    ],
    entry_points={
        'console_scripts': [
            'docs=visibl_docs.cli:main',
        ],
    },
    package_data={
        'visibl_docs': [
            'data/init_docs/**/*',
            'data/init_docs/**/.gitkeep',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    author="Visibl Team",
    description="Documentation generator for Verilog/SystemVerilog projects",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/visibl/docs",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
) 