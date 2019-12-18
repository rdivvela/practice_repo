from setuptools import setup, find_packages

setup(
    name="practice_repo",
    version="0.1.1",
    packages=find_packages(
        exclude=[
            "data/",
            "query_templates/",
            "scripts/",
        ]
    ),
    author="Ravi Divvela",
    install_requires=[
        "scikit-learn",
        "numpy",
        "click"
    ],
    entry_points = {
        "console_scripts": \
        ["new_repo=mapmove_relevance.mapmove_cli:map_relevance_score_cli"]
    }
)
