from setuptools import setup, find_packages

setup(
    name="notice_py",
    version="0.1.7",
    author="zefzhou44",
    author_email="zefzhou44@gmail.com",
    description="lark/sms/voice notice package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zefzhou/notice_py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.0",
    install_requires=[
        "requests", "alibabacloud_dysmsapi20170525", "tenacity",
        "python-dotenv"
    ],
)
