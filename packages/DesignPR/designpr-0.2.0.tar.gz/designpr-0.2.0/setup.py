from setuptools import setup, find_packages

setup(
    name="DesignPR",  
    version="0.2.0",  # Update as you make changes
    description="A GUI tool for designing PCR primers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="",
    author_email="",
    url="https://github.com/aidamo1824/DesignPR",  
    packages=find_packages(), 
    py_modules=["main"],
    entry_points={
        "console_scripts": [
            "run_DesignPR=designPR.main:main", 
        ],
    },
    license="MIT"
)
