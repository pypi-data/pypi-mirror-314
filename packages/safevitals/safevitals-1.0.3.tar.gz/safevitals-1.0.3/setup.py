from setuptools import setup, find_packages

setup(
    name="safevitals",
    version="1.0.3",
    author="Kavy",
    author_email="kavyvachhani@gmail.com",
    description="APK Vulnerability Scanner by Safe Vitals",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Kavyvachhani/safevitals",  # Replace with your GitHub URL
    packages=find_packages(),
    package_data={
        "safevitals": ["resources/jd-cli.jar"],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "reportlab",
        "matplotlib",
        "mobsfscan",
    ],
    entry_points={
        "console_scripts": [
            "safevitals=safevitals.scanner:main",
        ],
    },
)
