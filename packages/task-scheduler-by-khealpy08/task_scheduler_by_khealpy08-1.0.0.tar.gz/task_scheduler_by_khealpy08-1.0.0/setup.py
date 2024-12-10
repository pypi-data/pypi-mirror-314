from setuptools import setup, find_packages

setup(
    name="task_scheduler_by_khealpy08",
    version="1.0.0",
    description="A Task Scheduler application",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Michael Castil",
    author_email="castilmichael08@gmail.com",
    url="https://github.com/Khealgit08/taskscheduler",
    license="MIT",
    classifiers=["License :: OSI Approved :: MIT License",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9",
                 "Programming Language :: Python :: 3.10",
                 "Programming Language :: Python :: 3.11",
                 "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=["tkcalendar>=1.6.1,<2.0"],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "bson >= 0.5.10", 
            "twine>=4.0.2",
        ],
    },
    python_requires=">=3.7",
)
