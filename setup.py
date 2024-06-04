from setuptools import find_packages, setup

setup(
    name="Data Engineering",
    packages=find_packages(exclude=["tutorial_tests"]),
    install_requires=[
        "dagster",
        "dagster_duckdb_pandas",
        "dagster_duckdb",
        "dagster-cloud",
        "Faker==18.4.0",
        "matplotlib",
        "pandas",
        "requests",
        "feedparser",
        "beautifulsoup4",
        "pymongo",
        "polars",
        "streamlit",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
