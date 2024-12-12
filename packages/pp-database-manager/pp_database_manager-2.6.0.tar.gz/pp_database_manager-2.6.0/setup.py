from setuptools import find_packages, setup

setup(
    name="pp_database_manager",  # Package name
    version="2.6.0",  # Version number
    description="A database manager for Supabase and PocketBase",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Asman",
    packages=find_packages(),  # Automatically find sub-packages
    install_requires=[
        "pocketbase==0.12.0",  # Replace with the correct version
        "supabase==2.7.4",
        "python-dotenv",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
