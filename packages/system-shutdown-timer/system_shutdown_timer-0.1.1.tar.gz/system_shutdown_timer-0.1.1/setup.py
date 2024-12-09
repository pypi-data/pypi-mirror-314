from setuptools import setup, find_packages

setup(
    name="system_shutdown_timer",
    version="0.1.1",
    author="Himanshu Kumar Jha",
    author_email="himanshukrjha004@gmail.com",
    description="A library to set timers for closing apps and shutting down the system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/himanshu-kr-jha",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "shutdown-timer=system_shutdown_timer.timer:main",
        ],
    },
)
