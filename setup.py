from setuptools import setup

setup(
        name="sortuniq",
        version="0.2",
        description="Compute value counts of streaming input, displaying intermediate results.",
        author="adkein",
        author_email="adkein@gmail.com",
        packages=["sortuniq"],
        entry_points={
            "console_scripts": ["sortuniq = sortuniq.sortuniq:main"]
            },
        )
